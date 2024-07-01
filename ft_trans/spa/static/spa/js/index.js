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
    console.log('DOMContentLoaded No.3 tag:' + e.target.tagName);
    console.log('DOMContentLoaded No.3 class:' + e.target.className);


  document.getElementsByTagName('FORM')[0].addEventListener('submit', function(event) {
    console.log("FORM test No.1");
    event.preventDefault(); // フォームのデフォルトの送信を防止

    const form = event.target;
    const formData = new FormData(form);

  const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    fetch(form.action, {
      //ypmethod: form.method,
      method: "POST",
      headers: { 'X-CSRFToken': csrftoken
        //'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
       },
      mode: 'same-origin',
      body: formData
    })
    .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => console.log(data))
  .catch((error) => {
        console.log(error)
  })
    //.then(response => response.json())
    //.then(data => console.log(data))
    //.catch(error => console.error('Error:', error));
  });


    // Form送信
    if (e.target.tagName === 'BUTTON2' && e.target.className === 'form-button') {
      console.log('DOMContentLoaded No.5');
      e.preventDefault();

      console.log('DOMContentLoaded No.6');
      console.log('DOMContentLoaded No.6-1');
      const form = document.body.getElementsByTagName('form')[0];

      const inputs = form.getElementsByTagName('input');
      const textareas = form.getElementsByTagName('textarea');
      const selects = form.getElementsByTagName('select');

      const formData = new URLSearchParams();
      //const formData = new FormData();
      //const formData = new FormData()
      console.log("Add new test");
      //formData.set("test", "testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest");
      // 入力要素の値を取得
      for (let i = 0; i < inputs.length; i++) {
        if(inputs[i].value !== undefined){
          //formData.set(inputs[i].name, inputs[i].value);
          formData.append(inputs[i].name, inputs[i].value);
          console.log(`Input ${inputs[i].name}: ${inputs[i].value}`);
          //var input_data = document.createElement("input");
          //input_data.name = inputs[i].name;
          //input_data.value = inputs[i].value;
          //formData.appendChild(input_data);
        }

        //form.inputs[i].name = inputs[i].value;
      }

      // テキストエリアの値を取得
      for (let i = 0; i < textareas.length; i++) {

        if(textareas[i].value !== undefined){
          //formData.set(textareas[i].name, textareas[i].value);
          formData.append(textareas[i].name, textareas[i].value);
          //var input_data = document.createElement("input");
          //input_data.name = textareas[i].name;
          //input_data.value = textareas[i].value;
          //formData.appendChild(input_data);
        }

        //form.textareas[i].name = inputs[i].textareas[i].value;
        console.log(`Textarea ${textareas[i].name}: ${textareas[i].value}`);
      }

      // セレクトボックスの値を取得
      for (let i = 0; i < selects.length; i++) {
        if(selects[i].value !== undefined){
          //formData.set(selects[i].name, selects[i].value);
          formData.append(selects[i].name, selects[i].value);
          //var input_data = document.createElement("input");
          //input_data.name = selects[i].name;
          //input_data.value = selects[i].value;
          //formData.appendChild(input_data);
        }
        //form.selects[i].name = inputs[i].selects[i].value;
        console.log(`Select ${selects[i].name}: ${selects[i].value}`);
      }



      //console.log('DOMContentLoaded No.7 len:' + form.length);
      //const form2 = document.body.getElementsByClassName('form-button');
      //console.log('DOMContentLoaded No.7-2 len:' + form2.length);
      //let formData = new FormData(form[0]);
      console.log('DOMContentLoaded No.8');

      const url = form.action;
      console.log('DOMContentLoaded No.9');
      //console.table(form[0]);
      console.log('url:' + url);
      console.log('DOMContentLoaded No.12');
      //const url = '/account/signup/';
      //const view = new match.route.view();
      //const html = await view.getHtml();
      //document.querySelector('#app').innerHTML = html;


      //const form = document.getElementById('signup-form');
      //let formData = new FormData(form);
      //console.log('execute signup()');
      fetchAsForm(url, FormData, 'signup');
      //console.log('execute signup() end');

      //const current_uri = getDisplayedURI(tmp_path);
      //changingLanguage(lang_url, formData, current_uri);
      //changingLanguage(lang_url, form, current_uri);
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
