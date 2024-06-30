import { Routes } from './/routing/routes.js';
import { DataType } from './const/type.js';
import sendPost from './utility/post.js';
import { navigateTo, router } from './routing/routing.js';
import { changingLanguage } from './utility/lang.js';
import { getUrl } from './utility/url.js';
import { fetchAsForm } from './utility/fetch.js';

window.addEventListener('popstate', router);

const getDisplayedURI = (pathname) => {
  const splits = pathname.split('/').filter((uri) => uri !== '');
  let path = splits.find(
    (str) => Routes.findIndex((path) => path.path.replace('/', '') === str) >= 0
  );
  path = path === undefined ? '' : path;
  return getUrl(path);
};

document.addEventListener('DOMContentLoaded', () => {
  console.log('DOMContentLoaded No.1');
  let tmp_path = window.location.pathname;
  document.body.addEventListener('click', (e) => {
    // ページ切替
    if (e.target.matches('[data-link]')) {
      e.preventDefault();
      tmp_path = e.target.href;
      console.log('DOMContentLoaded No.2 tmp_path:' + tmp_path);
      navigateTo(tmp_path);
    }
    console.log('DOMContentLoaded No.3');

    // Form送信
    /*
    if (e.target.tagName === 'BUTTON' && e.target.className === 'form-button') {
      console.log('DOMContentLoaded No.5');
      e.preventDefault();

      console.log('DOMContentLoaded No.6');
      console.log('DOMContentLoaded No.6-1');
      const form = document.body.getElementsByTagName('form');
      //console.log('DOMContentLoaded No.7 len:' + form.length);
      //const form2 = document.body.getElementsByClassName('form-button');
      //console.log('DOMContentLoaded No.7-2 len:' + form2.length);
      //let formData = new FormData(form[0]);
      console.log('DOMContentLoaded No.8');

      const url = form[0].action;
      console.log('DOMContentLoaded No.9');
      //console.table(form[0]);
      console.log('url:' + url);
      console.log('DOMContentLoaded No.10');
      //const url = '/account/signup/';
      //const view = new match.route.view();
      //const html = await view.getHtml();
      //document.querySelector('#app').innerHTML = html;


      //const form = document.getElementById('signup-form');
      //let formData = new FormData(form);
      //console.log('execute signup()');
      fetchAsForm(url, form[0], 'signup');
      //console.log('execute signup() end');

      //const current_uri = getDisplayedURI(tmp_path);
      //changingLanguage(lang_url, formData, current_uri);
      //changingLanguage(lang_url, form, current_uri);
    }
    */

    //多言語切替
    if (e.target.tagName === 'INPUT' && e.target.className === 'change-language') {
      e.preventDefault();

      const lang_url = '/i18n/setlang/';
      const form = document.getElementById('lang_form');
      let formData = new FormData(form);
      const current_uri = getDisplayedURI(tmp_path);
      changingLanguage(lang_url, formData, current_uri);
      //changingLanguage(lang_url, form, current_uri);
    }
  });

  const uri = getDisplayedURI(tmp_path);
  navigateTo(uri);
  //router();
});
