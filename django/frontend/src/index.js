import { Routes } from './spa/js/routing/routes.js';
//import { navigateTo, router, updatePage } from './spa/js/routing/routing.js';
import { navigateTo, updatePage } from './spa/js/routing/routing.js';
import { changingLanguage } from './spa/js/utility/lang.js';
import { getUrl } from './spa/js/utility/url.js';
import { fetchAsForm } from './spa/js/utility/fetch.js';
//import { Pills } from 'bootstrap.bundle.min.js';
//import Cookies from 'js-cookie';
//import { Tooltip, Toast, Popover } from 'bootstrap';
import 'bootstrap';
import './accounts/js/two_fa.js';

import './spa/scss/spa.scss';
import './main.scss';

// パス名を取得する関数
const getDisplayedURI = (pathname) => {
  const splits = pathname.split('/').filter((uri) => uri !== '');
  let path = splits.find(
    (str) => Routes.findIndex((path) => path.path.replace('/', '') === str) >= 0
  );
  path = path === undefined ? '' : path;
  return getUrl(path);
};

document.addEventListener('DOMContentLoaded', () => {
  let tmp_path = window.location.pathname;
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
        //if (response && response !== '') {
        //const res = await response;
        //console.log('htmp:' + text);
        //response.then((data) => {
        updatePage(response);
        form.disabled = false;
        //});
        //}
      });
    }

    //多言語切替
    if (e.target.tagName === 'INPUT' && e.target.className === 'change-language') {
      e.preventDefault();

      const lang_url = '/i18n/setlang/';
      const form = document.getElementById('lang_form');
      let formData = new FormData(form);
      const current_uri = getDisplayedURI(tmp_path);
      changingLanguage(lang_url, formData, current_uri);
    }
  });

  const uri = getDisplayedURI(tmp_path);
  navigateTo(uri);
});
