import { Routes } from './spa/js/routing/routes.js';
import { navigateTo, updatePage } from './spa/js/routing/routing.js';
import { changingLanguage } from './spa/js/utility/lang.js';
import { getUrl } from './spa/js/utility/url.js';
import { fetchAsForm } from './spa/js/utility/fetch.js';

import './accounts/js/two_fa.js';
import './accounts/js/login.js';
import './accounts/js/signup.js';

import './spa/scss/spa.scss';
import './custom_bootstrap.scss';
import './main.scss';
import { loadNav } from './spa/js/utility/user.js';
//import 'login.js'

console.log('load index.js');

// パス名を取得する関数
export const getDisplayedURI = (pathname) => {
  const tmp_params = new URLSearchParams(window.location.search);
  const params = tmp_params == '' ? '' : '?' + tmp_params;
  const splits = pathname.split('/').filter((uri) => uri !== '');
  let path = splits.find(
    (str) => Routes.findIndex((path) => path.path.replace('/', '') === str) >= 0
  );
  path = path === undefined ? '' : path;
  if (path == '') {
    console.log('path is undefined');
    console.log('path is undefined');
    console.log('path is undefined');
    console.log('path is undefined');
    console.log('path is undefined');
    console.log('path is undefined');
    console.log('path is undefined');
    console.log('path is undefined');
    console.log('path is undefined');
  }

  let rest_path = '';
  if (path !== '') {
    // http://localhost/abc/def/ghi
    // 上記URLなら、/def/ghiがrest_pathとなる
    const test = splits.findIndex((tmp_path) => tmp_path == path);
    const slice_splits = splits.slice(test + 1);
    rest_path = '/' + slice_splits.join('/');
  }
  return { path: getUrl(path), rest: rest_path, params: params };
  //return getUrl(path);
};

document.addEventListener('DOMContentLoaded', async () => {
  loadNav();

  let tmp_path = window.location.pathname;
  console.log('tmp_path=' + tmp_path);

  document.body.addEventListener('click', (e) => {
    // ページ切替
    if (e.target.matches('[data-link]')) {
      e.preventDefault();
      tmp_path = e.target.href;
      navigateTo(tmp_path);
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
    }

    //多言語切替
    if (e.target.tagName === 'INPUT' && e.target.className === 'change-language') {
      e.preventDefault();

      const lang_url = '/i18n/setlang/';
      const form = document.getElementById('lang_form');
      let formData = new FormData(form);
      const current_uri = getDisplayedURI(tmp_path).path;
      changingLanguage(lang_url, formData, current_uri);
    }
  });

  console.log('No.2 tmp_path = ' + tmp_path);
  const uri = getDisplayedURI(tmp_path);
  console.log('uri = ' + uri.path);
  console.log('rest= ' + uri.rest);
  console.log('params= ' + uri.params);
  navigateTo(uri.path, uri.rest, uri.params);
});
