import '../scss/login.scss';
import { getUrlWithLang } from '../../spa/js/utility/url.js';
//import { fetchAsForm } from '../../spa/js/utility/fetch.js';
import { submitForm } from '../../spa/js/utility/form.js';
import { TwoFaEvent } from './two_fa.js';
import { handlePostLogin } from '../../spa/js/utility/user.js';
import ft_logo from '../assets/42.svg';

import { navModal } from './two_fa.js';
import { WebsocketInit } from '../../spa/js/ws/socket.js';
export const LoginEvent = new Event('LoginEvent');

function displayInstruction(id) {
  document.getElementById('instruction').hidden = true;
  document.getElementById('instruction-processing').hidden = true;
  document.getElementById('instruction-error').hidden = true;
  document.getElementById(id).hidden = false;
}
//const two_fa_form = document.getElementById('two-fa-verify-form');

document.addEventListener('LoginEvent', function () {
  const logo = document.querySelector('#ft-logo');
  if (logo == null) {
    return;
  }
  logo.src = ft_logo;

  try {
    // 入力があったらエラーメッセージを消去
    const input_elements = document
      .getElementById('login-form')
      .querySelectorAll('input,radio,select, button');
    input_elements.forEach((element) => {
      element.addEventListener('input', () => {
        document.getElementById('form-error').hidden = true;
      });
    });

    document.getElementById('login-form').addEventListener('submit', async function (event) {
      const response = await submitForm(event);
      /*
      event.preventDefault();
      const form = event.target;
      const formData = new FormData(form);
      const response = await fetchAsForm(form, formData);
      */

      if (response.status == 200) {
        const len = response.headers.get('Content-Length');
        if (len != undefined && len > 0) {
          try {
            const json = await response.json();
            const two_fa_form = document.getElementById('two-fa-verify-form');
            const resend_two_fa_form = document.getElementById('resend-two-fa');
            two_fa_form.action = getUrlWithLang('accounts/login-two-fa/');
            resend_two_fa_form.action = 'accounts/login-two-fa/';
            document.getElementById('app_url_qr').hidden = true;
            if (json['is_auth_app']) {
              document.getElementById('resend-button').hidden = true;
            }
            navModal(true);
            document.dispatchEvent(TwoFaEvent);
          } catch (error) {
            console.error(error);
            document.getElementById('form-error').hidden = false;
          }
        }
      } else {
        document.getElementById('form-error').hidden = false;
      }
    });

    document.getElementById('login-auth').addEventListener('click', async function () {
      const ft_oauth_url = document.getElementById('ft-oauth-url').href;
      displayInstruction('instruction-processing');

      try {
        //const url =
        //window.location.protocol + '//' + window.location.host + '/accounts/oauth-login';
        const url = getUrlWithLang('accounts/oauth-login');
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const res = await fetch(url, {
          method: 'POST',
          headers: { 'X-CSRFToken': csrftoken },
          mode: 'same-origin',
          body: JSON.stringify({ url: ft_oauth_url }),
          credentials: 'include',
        });
        if (res.status >= 400) {
          displayInstruction('instruction-error');
          document.getElementById('instruction').style.color = 'red';
          return '';
        }
        document.getElementById('close-modal').click();
        handlePostLogin();
        WebsocketInit();
      } catch (error) {
        displayInstruction('instruction-error');
        console.error('Fetch Error:' + error);
        return '';
      }
    });
  } catch (error) {
    console.error('Ignored:' + error.message);
  }
});
