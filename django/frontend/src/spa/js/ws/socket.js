import { setUserActive } from '../../../friend/js/friend.js';

let socket = null;

//const ws_url = 'ws://localhost:8001/ws';
const ws_url = 'ws://' + window.location.host + '/ws/websocket/';
console.log('ws_url=' + ws_url);

export const closetWebSocket = () => {
  socket.close();
};

export const sendWebSocket = async (json_message) => {
  console.log('sendWebSocket No.1 state:' + socket.readyState);
  if (socket == null || socket.readyState >= WebSocket.CLOSING) {
    socket = new WebSocket(ws_url);
  }
  console.log('sendWebSocket No.2 state:' + socket.readyState);

  socket.send(JSON.stringify(json_message));
  console.log('sendWebSocket No.3 state:' + socket.readyState);
};

export const WebsocketInit = () => {
  console.log('test No.1');

  if (socket == null || socket.readyState >= WebSocket.CLOSING) {
    socket = new WebSocket(ws_url);
  }

  // 接続が開かれた時の処理
  socket.onopen = function (event) {
    console.log('WebSocket connection opened.' + event);
    // サーバーにメッセージを送信
    //socket.send('Hello Server!');

    const chatMessage = {
      type: 'chat',
      message: 'Hello, this is a chat message.',
      arg: 'User1',
    };
    socket.send(JSON.stringify(chatMessage));
  };

  // サーバーからメッセージを受信した時の処理
  socket.onmessage = function (event) {
    console.log('Message from server:', event.data);

    var json = JSON.parse(event.data);
    //const json = JSON.stringify(event.data);
    const type = json['type'];
    const message = json['message'];
    console.log('Message from server type:', type);
    console.log('Message from server message:', message);

    if (type == 'get') {
      console.log('get No.1');
      if (message === 'Let me know your alive') {
        console.log('Let me know your alive');
        const resonse_json = { type: 'post', message: 'active' };
        sendWebSocket(resonse_json);
      } else if (message === 'game') {
        console.log('game');
      } else {
        console.log('Unknown message type');
      }
    } else if (type == 'post') {
      if (message === 'active_list') {
        const active_list = json['param1'];
        console.log('active_list:' + active_list);
        setUserActive(active_list);
      }
      console.log('post No.2');
    } else {
      console.log('other No.3');
    }
  };

  socket.onclose = function (event) {
    console.error('WebSocket closed unexpectedly:', event);
  };

  // エラーが発生した時の処理
  socket.onerror = function (event) {
    console.error('WebSocket error observed:', event);
  };
};
export const WebsocketInit0 = () => {
  if (socket == null) {
    socket = new WebSocket(ws_url);
  }
  //socket = new WebSocket('wss://example.com/ws/chat/');
  console.log('WebsocketInit No.1');
  //if (socket.readyState === WebSocket.OPEN) {

  //reconnect();
  //console.log('WebsocketInit No.2');
  // 接続済みなので何もしない
  //return;
  //}
  /*
  socket.addEventListener('message', function (event) {
    console.log('メッセージを受信:', event.data);
  });
  socket.addEventListener('error', function (event) {
    console.error('WebSocketエラーが発生しました', event);
  });
  socket.addEventListener('close', function (event) {
    console.log('WebSocketは切断されました' + event);
  });
  socket.addEventListener('open', function (event) {
    console.log('WebSocketは接続されています' + event);
  });
  */

  // WebSocket接続が開かれたときの処理
  socket.onopen = function () {
    console.log('WebSocket connection opened.');

    /*
    // チャットメッセージの送信
    const chatMessage = {
      type: 'chat',
      content: 'Hello, this is a chat message.',
      sender: 'User1',
    };
    socket.send(JSON.stringify(chatMessage));

    // 通知の送信
    const notification = {
      type: 'notification',
      content: 'You have a new notification.',
      recipient: 'User1',
    };
    socket.send(JSON.stringify(notification));
    */
  };

  // メッセージを受け取ったときの処理
  //socket.onmessage = function (data) {
  socket.onmessage = function (event) {
    console.log('receive WS No.0:');
    console.log('receive WS No.1:' + event);
    //const message = JSON.parse(event);
    console.log('receive WS No.2 type:' + event.type);
    console.log('receive WS No. message:' + event.message);

    // メッセージのタイプで分岐
    switch (event.type) {
      case 'chat':
        console.log('chat');
        //console.log('Chat message received: ' + message.content);
        break;
      case 'notification':
        console.log('notification');
        //console.log('Notification received: ' + message.content);
        break;
      case ' check':
        console.log('check');
        //console.log('Notification received: ' + message.content);
        break;
      default:
        console.log('Unknown message type');
    }
  };

  // WebSocket接続が閉じられたときの処理
  socket.onclose = function () {
    console.log('WebSocket connection closed. and re-open');
    setTimeout(function () {
      WebsocketInit(); // 5秒後に再接続
    }, 5000);
  };

  // エラー発生時の処理
  socket.onerror = function (error) {
    console.log('WebSocket error: ', error);
  };

  console.log('WebsocketInit End ');
};
