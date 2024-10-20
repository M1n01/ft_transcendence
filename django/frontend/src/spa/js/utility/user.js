import { fetchAsForm } from './fetch.js';
import { router } from '../routing/routing.js';
import { navigateTo } from '..//routing/routing.js';
import { moveTo } from '../routing/routing.js';
import { getDisplayedURI } from '../../../../src/index.js';
import { closetWebSocket } from '../ws/socket.js';
import { loadNav } from './navi.js';

export function isLogined() {
  //todo
  // ログインしていればtrue
  // ログインしていなければfalseを返す

  return true;
}

export const reload = async () => {
  const uri = getDisplayedURI(window.location.href);
  await router(uri.rest, uri.params);
  await loadNav();
};

export const handlePostLogin = async () => {
  moveTo('/games');
  document.getElementById('nav').hidden = false;
};

export const logout = async () => {
  const form = document.getElementById('nav-logout-form');
  const formData = new FormData(form);
  const response = await fetchAsForm(form, formData);
  if (response.status == 200) {
    closetWebSocket();
    navigateTo('login-signup');
    await reload();
  }
};
