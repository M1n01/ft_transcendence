import { fetchAsForm } from '../../spa/js/utility/fetch.js';
import '../scss/two_fa.scss';
export const TwoFaEvent = new Event('TwoFaEvent');
//import { updatePage } from './routing/routing.js';
function displayInput(id) {
  document.getElementById('input_email').hidden = true;
  document.getElementById('input_sms').hidden = true;
  document.getElementById('input_app').hidden = true;
  document.getElementById(id).hidden = false;
}

function copyInput() {
  if (document.getElementById('option_email').checked == true) {
    document.getElementById('common-mode').value = document.getElementById('option_email').value;
    document.getElementById('common-input').value = document.getElementById('email_address').value;
  } else if (document.getElementById('option_sms').checked == true) {
    document.getElementById('common-mode').value = document.getElementById('option_sms').value;
    document.getElementById('common-input').value = document.getElementById('phone_number').value;
  } else if (document.getElementById('option_app').checked == true) {
    document.getElementById('common-mode').value = document.getElementById('option_app').value;
    document.getElementById('common-input').value = document.getElementById('app_name').value;
  }
}

function switchingAllInput(mode) {
  if (mode) {
    document.getElementById('input_email').disable = true;
    document.getElementById('input_sms').disable = true;
    document.getElementById('input_app').disable = true;
    //const radioButtons = document.querySelectorAll('input[name="mode"]');
    const radioButtons = document.querySelectorAll('input');
    radioButtons.forEach(function (radioButton) {
      radioButton.disabled = true;
    });

    document.getElementById('two-fa-submit').hidden = true;
    document.getElementById('verify-input').hidden = false;
    document.getElementById('verify-code').disabled = false;
    document.getElementById('verify-submit').disabled = false;
    document.getElementById('common-mode').disabled = false;
    document.getElementById('common-input').disabled = false;
  } else {
    document.getElementById('input_email').disable = false;
    document.getElementById('input_sms').disable = false;
    document.getElementById('input_app').disable = false;
    //const radioButtons = document.querySelectorAll('input[name="mode"]');
    const radioButtons = document.querySelectorAll('input');
    radioButtons.forEach(function (radioButton) {
      radioButton.disabled = false;
    });

    document.getElementById('two-fa-submit').hidden = false;
    document.getElementById('verify-input').hidden = true;
    document.getElementById('verify-code').disabled = true;
    document.getElementById('verify-submit').disabled = true;
    document.getElementById('common-mode').disabled = true;
    document.getElementById('common-input').disabled = true;
  }
}

document.addEventListener('TwoFaEvent', function () {
  console.log('2FA Event Test');
  document.getElementById('two_fa_form').addEventListener('submit', async function (event) {
    event.preventDefault(); // フォームのデフォルトの送信を防止
    const form = event.target;
    console.log('2fa Test');
    console.log('2FA Click Test');
    const formData = new FormData(form);
    const response = await fetchAsForm(form, formData);
    if (response.status == 200) {
      document.getElementById('failure-send-2fa').hidden = true;
      console.log('response status 200');
      switchingAllInput(true);
      copyInput();
    } else {
      console.log('response status ERROR:' + response.status);
      document.getElementById('failure-send-2fa').hidden = false;
      //window.
    }
  });

  document.getElementById('two_fa_verify_form').addEventListener('submit', async function (event) {
    event.preventDefault(); // フォームのデフォルトの送信を防止
    const form = event.target;
    //console.log('2fa Test');
    //console.log('2FA Click Test');
    const formData = new FormData(form);
    console.table(formData);
    const response = await fetchAsForm(form, formData);
    if (response.status == 200) {
      console.log('response status 200');
      switchingAllInput(true);
      document.querySelector('#app').innerHTML = await response.text();
    } else {
      console.log('response status ERROR:' + response.status);
      document.getElementById('failure-verify').hidden = false;
      //window.
    }
  });

  const RadioEmail = document.getElementById('option_email');
  const RadioSMS = document.getElementById('option_sms');
  const RadioApp = document.getElementById('option_app');
  const Resend = document.getElementById('resend');
  const VerifyInput = document.getElementById('verify-code');

  //const VerifySubmit = document.getElementById('verify-submit');
  RadioEmail.addEventListener('change', function () {
    displayInput('input_email');
  });
  RadioSMS.addEventListener('change', function () {
    displayInput('input_sms');
  });
  RadioApp.addEventListener('change', function () {
    displayInput('input_app');
  });
  Resend.addEventListener('click', function () {
    switchingAllInput(false);
    document.getElementById('verify-code').value = '';
  });

  RadioSMS.addEventListener('change', function () {
    displayInput('input_sms');
  });
  VerifyInput.addEventListener('input', function () {
    document.getElementById('failure-verify').hidden = true;
    //copyInput();
  });
  /*
  VerifySubmit.addEventListener('click', function () {
    console.log('click');
    copyInput();
  });
  */
});
