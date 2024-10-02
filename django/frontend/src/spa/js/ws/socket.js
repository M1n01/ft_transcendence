import { setUserActive } from '../../../friend/js/friend.js';

let socket = null;
const ws_url = 'ws://' + window.location.host + '/ws/websocket/';

export const closetWebSocket = () => {
  socket.close();
};

export const sendWebSocket = async (json_message) => {
  if (socket == null || socket.readyState >= WebSocket.CLOSING) {
    socket = new WebSocket(ws_url);
  }
  socket.send(JSON.stringify(json_message));
};

export const WebsocketInit = () => {
  if (socket == null || socket.readyState >= WebSocket.CLOSING) {
    socket = new WebSocket(ws_url);
  }

  // 接続が開かれた時の処理
  socket.onopen = function (event) {
    console.log('Websocket Open:' + event);
  };

  // サーバーからメッセージを受信した時の処理
  socket.onmessage = function (event) {
    var json = JSON.parse(event.data);
    const type = json['type'];
    const message = json['message'];

    if (type == 'get') {
      if (message === 'Let me know your alive') {
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
        setUserActive(active_list);
      }
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
