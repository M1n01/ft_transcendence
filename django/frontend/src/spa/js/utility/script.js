//import { TwoFaEvent } from '../../../accounts/js/two_fa.js';
//import { LoginEvent } from '../../../accounts/js/login.js';
//import { SignupEvent } from '../../../accounts/js/signup.js';

export function executeScriptTab(path) {
  const app = document.querySelector('#app');
  var newDiv = document.createElement('script');
  const id = 'script' + path;

  // すでに<script>タグがあれば削除する
  if (document.getElementById(id)) {
    document.getElementById(id).remove();
  }

  var script = app.getElementsByTagName('script');
  if (script !== undefined && script[0] !== undefined) {
    if (script[0].src && script[0].src !== '') {
      newDiv.src = script[0].src;
    } else if (script[0].innerHTML !== '') {
      newDiv.textContent = script[0].innerHTML;
    } else {
      newDiv.src = path;
    }
    newDiv.id = id;
    document.body.appendChild(newDiv);
  }
}
