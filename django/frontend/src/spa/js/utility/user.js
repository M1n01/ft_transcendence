import { fetchAsForm } from './fetch.js';
import { router } from '../routing/routing.js';
import { getUrlWithLang } from './url.js';
import fetchData from './fetch.js';
import { navigateTo } from '..//routing/routing.js';
//import 'bootstrap';
import { Dropdown } from 'bootstrap';

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

    const small_menu_icon = document.getElementById('small_menu_icon');
    //var navbarToggler = document.querySelector('.navbar-toggler');
    const dropdown = document.getElementById('small-menu-dropdown');

    const isExpanded = small_menu_icon.getAttribute('aria-expanded') === 'true';
    console.log('test No.1');

    small_menu_icon.addEventListener('click', async () => {
      console.log('test No.2');
      if (!isExpanded) {
        console.log('test No.3');
        // Bootstrapのdropdownメソッドに相当するコードを実装
        var dropdownMenu = new Dropdown(dropdown);
        console.log('test No.4');
        dropdownMenu.toggle();
        console.log('test No.5');
      }
      console.log('test No.6');

      //await logout();
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
    navigateTo('login-signup');
    //history.pushState(null, null, 'login-signup');
    await reload();
    //document.getElementById('nav').hidden = true;
  }
};
