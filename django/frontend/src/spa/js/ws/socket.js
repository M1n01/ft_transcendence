const socket = new WebSocket('ws://localhost:8001/ws');

export const WebsocketInit = () => {
  console.log('ws init() No.1');
  if (socket.readyState === WebSocket.OPEN) {
    console.log('ws init() No.2');
    // 接続済みなので何もしない
    return;
  }
  console.log('ws init() No.3');
  // WebSocket接続が開かれたときの処理
  socket.onopen = function () {
    console.log('WebSocket connection opened.');

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
  };

  // メッセージを受け取ったときの処理
  socket.onmessage = function (event) {
    const message = JSON.parse(event.data);

    // メッセージのタイプで分岐
    switch (message.type) {
      case 'chat':
        console.log('Chat message received: ' + message.content);
        break;
      case 'notification':
        console.log('Notification received: ' + message.content);
        break;
      default:
        console.log('Unknown message type');
    }
  };

  // WebSocket接続が閉じられたときの処理
  socket.onclose = function () {
    console.log('WebSocket connection closed.');
  };

  // エラー発生時の処理
  socket.onerror = function (error) {
    console.log('WebSocket error: ', error);
  };
};
