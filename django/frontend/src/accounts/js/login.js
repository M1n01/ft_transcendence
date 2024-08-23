import '../scss/login.scss';
import { fetchAsForm } from '../../spa/js/utility/fetch.js';
import { TwoFaEvent } from './two_fa.js';

function displayInstruction(id) {
  document.getElementById('instruction').hidden = true;
  document.getElementById('instruction-processing').hidden = true;
  document.getElementById('instruction-error').hidden = true;
  document.getElementById(id).hidden = false;
}

function switchingForm(flag) {
  const login_form = document.getElementById('login-form');
  const login_form_elements = login_form.querySelectorAll('input,radio,select, button');
  const dialog = document.getElementById('openDialog');
  const back_button = document.getElementById('back-button');
  const code_input = document.getElementById('verify-code');

  if (flag) {
    dialog.disabled = true;
    back_button.hidden = false;
    login_form_elements.forEach((element) => {
      element.readOnly = true;
    });
    login_form.action = 'accounts/login/';
    code_input.hidden = false;
    code_input.disabled = false;
    code_input.readOnly = false;
  } else {
    dialog.disabled = false;
    back_button.hidden = true;
    login_form_elements.forEach((element) => {
      element.readOnly = false;
    });
    login_form.action = 'accounts/login-tmp/';
    code_input.hidden = true;
    code_input.disabled = true;
  }
}

export const LoginEvent = new Event('LoginEvent');

document.addEventListener('LoginEvent', function () {
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
      event.preventDefault();
      const form = event.target;
      const formData = new FormData(form);
      const response = await fetchAsForm(form, formData);

      if (response.status == 200) {
        switchingForm(true);
        const len = response.headers.get('Content-Length');
        if (len != undefined && len > 0) {
          document.querySelector('#app').innerHTML = await response.text();
          document.dispatchEvent(TwoFaEvent);
        }
      } else {
        //document.querySelector('#app').innerHTML = await response.text();
        document.getElementById('form-error').hidden = false;
      }
    });

    // 42 OAuth
    //document.getElementById('openDialog').addEventListener('click', function () {
    //document.getElementById('myDialog').showModal();
    //});
    document.getElementById('back-button').addEventListener('click', function () {
      switchingForm(false);
    });

    document.getElementById('closeDialog').addEventListener('click', async function () {
      const ft_oauth_url = document.getElementById('ft-oauth-url').href;
      displayInstruction('instruction-processing');

      try {
        const url =
          window.location.protocol + '//' + window.location.host + '/accounts/oauth-login/';
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
        //document.getElementById('myDialog').close();
        document.getElementById('close-modal').click();
        document.getElementById('success-login').click();
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
