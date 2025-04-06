import json
import re
import boto3
import pandas as pd
import simplejson as json
from decimal import Decimal
from google.cloud import storage

def food_order(request):
    session = boto3.Session(
        aws_access_key_id='',
        aws_secret_access_key='',
        aws_session_token='',
        region_name='us-east-1'
    )
    print('session valid', session)

    storage_client = storage.Client()
    bucket = storage_client.bucket('serverless-visualisation')
    print('got bucket')
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table('FoodOrders')
    
    response = table.scan()
    print('db res: ', response)
    result = response['Items']
    print('result: ', result)
    df = pd.DataFrame(result)
    grouped = df.groupby(df['date'])
    resultDf = pd.DataFrame()
    resultDf1 = pd.DataFrame()
    resultDf2 = pd.DataFrame()

    for name,group in grouped:
      print(name)
      print(len(group))
      row = {'dates': name , 'num_of_orders': len(group)}
      resultDf = resultDf.append(row, ignore_index = True)
      row1 = {'dates': name , 'total_ammount': group['price'].sum()}
      resultDf1 = resultDf1.append(row1, ignore_index = True)

    grouped1 = df.groupby(df['foodItems'])
    for name,group in grouped1:
      row2 = {'items': name , 'num_of_orders':   len(group)}
      resultDf2 = resultDf2.append(row2, ignore_index = True)

    bucket.blob('food_order.csv').upload_from_string(resultDf.to_csv(index=False), 'text/csv')
    bucket.blob('food_order1.csv').upload_from_string(resultDf1.to_csv(index=False), 'text/csv')
    bucket.blob('food_order2.csv').upload_from_string(resultDf2.to_csv(index=False), 'text/csv')



    print(result)
    return {
        'statusCode': 200,
        'body': json.dumps(result,use_decimal=True),
        'message': 'csv generated'
    }