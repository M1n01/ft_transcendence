import { Routes } from './/routing/routes.js';
import { DataType } from './const/type.js';
import sendPost from './utility/post.js';
import { navigateTo, router, updatePage } from './routing/routing.js';
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
    console.log('DOMContentLoaded No.3 tag:' + e.target.tagName);
    console.log('DOMContentLoaded No.3 class:' + e.target.className);


    const document_form = document.getElementsByTagName('FORM');
    if(document_form &&  document_form.length  > 0){
  document.getElementsByTagName('FORM')[0].addEventListener('submit', function(event) {
    event.preventDefault(); // フォームのデフォルトの送信を防止

    const form = event.target;
    const formData = new FormData(form);
    console.log("start fetchAsForm");
    const response = fetchAsForm(form, formData);
    if(response && response !== ""){
      console.log("end fetchAsForm response is");
      response.then(data => {
        console.log("data=[" + data + "]");
      updatePage(data);
        }
      );
      console.log("end fetchAsForm response is not error");
    }
    console.log("end fetchAsForm");
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
      //changingLanguage(lang_url, form, current_uri);
    }
  });

  const uri = getDisplayedURI(tmp_path);
  navigateTo(uri);
  //router();
});
