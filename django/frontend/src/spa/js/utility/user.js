import { fetchAsForm } from './fetch.js';
import { router } from '../routing/routing.js';

export function isLogined() {
  //todo
  // ログインしていればtrue
  // ログインしていなければfalseを返す

  return true;
}

export const reload = async () => {
  await router();
};

export const logout = async () => {
  const form = document.getElementById('nav-logout-form');
  const formData = new FormData(form);
  const response = await fetchAsForm(form, formData);
  if (response.status == 200) {
    document.getElementById('nav').hidden = true;
    await reload();
  }
};

//const reload = async () => {
//      router();
//};
