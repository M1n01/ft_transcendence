import { fetchAsForm } from './fetch.js';
import { router } from '../routing/routing.js';
import { getUrlWithLang } from './url.js';
import fetchData from './fetch.js';

export function isLogined() {
  //todo
  // ログインしていればtrue
  // ログインしていなければfalseを返す

  return true;
}

export const reload = async () => {
  await router();
  await loadNav();
};

export const loadNav = async () => {
  try {
    const nav_uri = getUrlWithLang('spa/nav');
    const nav_html = await fetchData(nav_uri);
    document.querySelector('#nav').innerHTML = nav_html;

    const logout_button = document.getElementById('nav-logout-button');
    logout_button.addEventListener('click', async () => {
      await logout();
    });
  } catch (error) {
    console.log('ignore error:' + error);
  }
};

export const handlePostLogin = async () => {
  await reload();
  document.getElementById('nav').hidden = false;
};

export const logout = async () => {
  const form = document.getElementById('nav-logout-form');
  const formData = new FormData(form);
  const response = await fetchAsForm(form, formData);
  if (response.status == 200) {
    await reload();
    document.getElementById('nav').hidden = true;
  }
};
