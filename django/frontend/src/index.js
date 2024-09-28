import { Routes } from './spa/js/routing/routes.js';
//import { router } from './spa/js/routing/routing.js';
import { navigateTo, updatePage, savePage } from './spa/js/routing/routing.js';
import { changingLanguage } from './spa/js/utility/lang.js';
import { getUrl } from './spa/js/utility/url.js';
import { fetchAsForm } from './spa/js/utility/fetch.js';

import './accounts/js/two_fa.js';
import './accounts/js/login.js';
import './accounts/js/signup.js';

import './spa/scss/spa.scss';
import './custom_bootstrap.scss';
import './main.scss';
import { WebsocketInit } from './spa/js/ws/socket.js';
import { loadNav } from './spa/js/utility/user.js';
//import 'login.js'

// パス名を取得する関数
export const getDisplayedURI = (pathname) => {
  let query_index = pathname.lastIndexOf('?');
  console.log('No.1 query_index:' + query_index);
  if (pathname.lastIndexOf('/') > query_index) {
    console.log('No.2 query_index:' + query_index);
    query_index = 0;
  }

  const params = query_index == 0 ? '' : pathname.substring(query_index);
  console.log('No.3 params:' + params);
  pathname.replace(params, '');
  const splits = pathname.split('/').filter((uri) => uri !== '');
  let path = splits.find(
    (str) => Routes.findIndex((path) => path.path.replace('/', '') === str) >= 0
  );
  path = path === undefined ? '' : path;

  let rest_path = '';
  if (path !== '') {
    // http://localhost/abc/def/ghi
    // 上記URLなら、/def/ghiがrest_pathとなる
    const test = splits.findIndex((tmp_path) => tmp_path == path);
    const slice_splits = splits.slice(test + 1);
    rest_path = '/' + slice_splits.join('/');
  }

  console.log('getDisplayedURI No.0 rest:' + rest_path);
  rest_path = rest_path.replace(params, '');
  console.log('getDisplayedURI No.1 rest:' + rest_path);
  if (rest_path === '/') {
    rest_path = '';
  }
  console.log('getDisplayedURI No.2 rest:' + rest_path);
  if (params.length > 0 && rest_path.length > 0) {
    if (rest_path[rest_path.length - 1] == '/') {
      rest_path = rest_path.substring(0, rest_path.length - 1);
    }
  }
  console.log('getDisplayedURI No.3 rest:' + rest_path);
  return { path: getUrl(path), rest: rest_path, params: params };
};

document.addEventListener('DOMContentLoaded', async () => {
  loadNav();
  WebsocketInit();

  let tmp_path = window.location.pathname;

  document.body.addEventListener('click', (e) => {
    // ページ切替
    if (e.target.matches('[data-link]')) {
      savePage(window.location.href);

      e.preventDefault();
      tmp_path = e.target.href;
      const uri = getDisplayedURI(tmp_path);
      navigateTo(uri.path, uri.rest, uri.params);
    }

    // Form送信
    const document_form = document.getElementsByTagName('FORM');
    if (document_form && document_form.length > 0) {
      document.getElementsByTagName('FORM')[0].addEventListener('submit', async function (event) {
        event.preventDefault(); // フォームのデフォルトの送信を防止
        const form = event.target;
        if (form.disabled == true) {
          //なぜか２回以上実行される（Formも２回以上送信される）ため、
          //ここで無効化させる。
          return;
        }

        form.disabled = true;

        const formData = new FormData(form);
        const response = await fetchAsForm(form, formData);
        updatePage(response);
        form.disabled = false;
      });

      //多言語切替
      if (e.target.tagName === 'INPUT' && e.target.className === 'change-language') {
        e.preventDefault();

        const lang_url = '/i18n/setlang/';
        const form = document.getElementById('lang_form');
        let formData = new FormData(form);
        const current_uri = getDisplayedURI(tmp_path).path;
        changingLanguage(lang_url, formData, current_uri);
      }
    }
  });

  const uri = getDisplayedURI(tmp_path);
  navigateTo(uri.path, uri.rest, uri.params);
});
