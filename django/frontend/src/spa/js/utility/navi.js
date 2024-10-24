import { getUrlWithLang } from './url.js';
import fetchData from './fetch.js';
import { logout } from './user.js';
import { sendWebSocket } from '../ws/socket.js';
import { fetchJsonData } from '../utility/fetch.js';
const NOTIFICATION_INTERVAL = 10000;

export const UpdateMessageIcon = (cnt, ws = false) => {
  const cnt_str = document.getElementById('alerm-number');
  const svg = document.getElementById('navi-alert-icon-svg');
  if (cnt_str) {
    cnt_str.hidden = false;
    svg.style.fill = 'white';

    if (ws == false) {
      cnt = Number(cnt_str.textContent);
    }

    if (cnt > 99) {
      cnt_str.textContent = '99+';
    } else if (cnt > 0) {
      cnt_str.textContent = cnt;
    } else {
      cnt_str.hidden = true;
      svg.style.fill = 'gray';
    }
  }
};

function getNotificationCount() {
  const message = {
    type: 'get',
    message: 'alert_cnt',
  };
  sendWebSocket(message);
  return 0;
}

export let GetNotificationInterval = setInterval(getNotificationCount, NOTIFICATION_INTERVAL);

export const loadNav = async () => {
  try {
    const json = await fetchJsonData('/spa/is-login');
    if (json['is_redirect'] == true) {
      return;
    }

    const nav_uri = getUrlWithLang('spa/nav');
    const nav_html = await fetchData(nav_uri);
    document.querySelector('#nav').innerHTML = nav_html;

    const logout_button = document.getElementById('nav-logout-button');
    logout_button.addEventListener('click', async () => {
      await logout();
    });

    const logout_button_sm = document.getElementById('nav-logout-button-sm');
    logout_button_sm.addEventListener('click', async () => {
      await logout();
    });
    UpdateMessageIcon(0, false);
    GetNotificationInterval;
  } catch (error) {
    console.log('ignore error:' + error);
  }
};
