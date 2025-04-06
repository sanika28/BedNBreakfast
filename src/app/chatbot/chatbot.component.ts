import { Component, OnInit } from '@angular/core';
import { LexRuntime } from 'aws-sdk';
import { Message } from './message.model';

@Component({
  selector: 'app-chatbot',
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.scss']
})
export class ChatbotComponent implements OnInit {
  lexRuntime = new LexRuntime();
  userInput: string = '';
  chatMsg: Message[] = [];
  initState: string | undefined = 'Hi, How Can I help you';
  messages: any;
  constructor() { }

  ngOnInit(): void {
    this.messages.push(new Message(this.initState?.toString(), 'Bot'));
  }

  postMessage() {
    var params = {
      botAlias: 'beta',
      botName: 'BandB',
      inputText: 'flowers',
      userId: 'user1986318',
    };

    this.lexRuntime = new LexRuntime({
      accessKeyId: '',
      secretAccessKey: '',
      sessionToken: '',
      region: 'us-east-1'
    });
    params.inputText = this.userInput;
    this.lexRuntime.postText(params, (err, data) => {
      if (err) {
        console.log(err, err.stack); // an error occurred
      }
      else {
        this.initState = data.message;
      }
      this.chatMsg.push(new Message(this.userInput, 'You'));
      this.userInput = "";
      this.chatMsg.push(new Message(this.initState, 'Bot'));
    }
    );
  }
}
