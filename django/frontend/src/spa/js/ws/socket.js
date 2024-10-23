import { setUserActive } from '../../../friend/js/friend.js';
import { UpdateMessageIcon } from '../utility/navi.js';
import { fetchJsonData } from '../utility/fetch.js';

let socket = null;
let ws_url = 'wss://' + window.location.host + '/ws/websocket/';
if (window.location.protocol == 'http:') {
  ws_url = 'ws://' + window.location.host + '/ws/websocket/';
}

export const closetWebSocket = () => {
  if (socket) {
    socket.close();
  }
};

export const sendWebSocket = async (json_message) => {
  if (socket == null || socket.readyState >= WebSocket.CLOSING) {
    try {
      const json = await fetchJsonData('/spa/is-login');
      if (json['is_redirect'] == false) {
        socket = new WebSocket(ws_url);
      }
    } catch {
      return;
    }
  }

  if (socket != null && socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify(json_message));
  }
};

export const WebsocketInit = async () => {
  if (socket == null || socket.readyState >= WebSocket.CLOSING) {
    try {
      const json = await fetchJsonData('/spa/is-login');
      if (json['is_redirect'] == false) {
        socket = new WebSocket(ws_url);
      }
    } catch {
      return;
    }
  }

  // 接続が開かれた時の処理
  /*
  socket.onopen = function (event) {
    console.log('Websocket Open:' + event);
  };
  */

  // サーバーからメッセージを受信した時の処理
  if (socket) {
    socket.onmessage = function (event) {
      try {
        var json = JSON.parse(event.data);
        const type = json['type'];
        const message = json['message'];

        if (type == 'get') {
          if (message === 'Let me know your alive') {
            const resonse_json = { type: 'post', message: 'active' };
            sendWebSocket(resonse_json);
          } else if (message === 'game') {
            //console.log('game');
          } else {
            //console.log('Unknown message type');
          }
        } else if (type == 'post') {
          if (message === 'active_list') {
            const active_list = json['param1'];
            setUserActive(active_list);
          } else if (message === 'alert_cnt') {
            const cnt = json['param1'];
            UpdateMessageIcon(cnt, true);
          }
        }
      } catch (error) {
        console.error('Ignore error:' + error);
      }
    };
  }

  /*
  socket.onclose = function (event) {
    //console.error('WebSocket closed unexpectedly:', event);
  };

  // エラーが発生した時の処理
  socket.onerror = function (event) {
    //console.error('WebSocket error observed:', event);
  };
  */
};
