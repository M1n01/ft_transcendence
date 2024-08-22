import '../scss/signup.scss';
import { fetchAsForm } from '../../spa/js/utility/fetch.js';
import { SignupTwoFAEvent } from './signup_two_fa.js';
export const SignupEvent = new Event('SignupEvent');

//function copyInput() {
//  const two_fa = document.getElementById('id_auth');
//  document.getElementById('common-mode').value = two_fa.value;
//  if (two_fa.value == 'SMS') {
//    document.getElementById('common-input').value =
//      document.getElementById('id_country_code').value + document.getElementById('id_phone').value;
//  } else {
//    document.getElementById('common-input').value = document.getElementById('id_email').value;
//  }
//}

//function switchingTwoFA(mode) {
//  const signup_form = document.getElementById('signup-form');
//  const signup_form_elements = signup_form.querySelectorAll('input,radio,select, button');
//  const two_fa_button = document.getElementById('2fa-button');
//  const two_fa_form = document.getElementById('two-fa-form');
//  const back_button = document.getElementById('back-button');
//  if (mode) {
//    signup_form_elements.forEach((element) => {
//      element.disabled = true;
//    });
//    back_button.disabled = false;
//    two_fa_button.hidden = false;
//    two_fa_form.hidden = false;
//    two_fa_form.action = '/accounts/two-fa-verify/';
//    back_button.hidden = false;
//  } else {
//    signup_form_elements.forEach((element) => {
//      element.disabled = false;
//    });
//    back_button.disabled = true;
//    two_fa_button.hidden = true;
//    two_fa_form.hidden = true;
//    two_fa_form.action = '/accounts/two-fa/';
//    back_button.hidden = true;
//  }
//}

function SetTime() {
  const Mytoday = new Date();
  const yyyy = Mytoday.getFullYear();
  const mm = String(Mytoday.getMonth() + 1).padStart(2, '0');
  const dd = String(Mytoday.getDate()).padStart(2, '0');
  const todayString = `${yyyy}-${mm}-${dd}`;
  document.getElementById('id_created_at').value = todayString;
  document.getElementById('id_birth_date').type = 'date';
}

document.addEventListener('SignupEvent', function () {
  SetTime();

  const signup_form = document.getElementById('signup-form');
  const two_fa_button = document.getElementById('2fa-button');

  const auth_select = document.getElementById('id_auth');
  const phone_input = document.getElementById('id_phone');
  const phone_auth_error = document.getElementById('phone-auth-error');
  //const submit_button = document.getElementById('validation-button');
  signup_form.addEventListener('submit', async function (e) {
    e.preventDefault();
    if (auth_select.value == 'SMS' && phone_input.value == '') {
      phone_auth_error.hidden = false;
      return;
    }
    const form = e.target;
    const formData = new FormData(form);
    let response = await fetchAsForm(form, formData);
    const json = await response.json();
    document.querySelector('#app').innerHTML = json.html;
    if (json['valid'] == false) {
      document.dispatchEvent(SignupEvent);
      return;
    }
    //document.querySelector('#app').innerHTML = json.html;
    document.dispatchEvent(SignupTwoFAEvent);

    //form.action = '/accounts/signup-tmp/';
    //response = await fetchAsForm(form, formData);

    /*
    phone_auth_error.hidden = true;
    const form = e.target;
    form.action = '/accounts/signup-valid/';

    const formData = new FormData(form);
    const response = await fetchAsForm(form, formData);
    const html = await response.text();

    if (response.status == 200) {
      document.getElementById('server-error').hidden = true;
      document.querySelector('#app').innerHTML = html;
      return;
    } else if (response.status == 400) {
      document.querySelector('#app').innerHTML = html;
      document.dispatchEvent(SignupEvent);

      return;
      /*
      if (json['valid'] == undefined || json['valid'] == false) {
        document.dispatchEvent(SignupEvent);
        return;
      }
    } else {
      document.getElementById('server-error').hidden = false;
      return;
    }
    */

    /*
    // ここからさきはバリデーションが成功したら実行される
    const errors = document.querySelectorAll('.errorlist');
    errors.forEach((element) => {
      element.style.display = 'none';
      element.hidden = true;
    });

    const flag = true;
    if (flag) {
      copyInput();
      const two_fa_form = document.getElementById('two-fa-form');
      const formData = new FormData(two_fa_form);
      const response = await fetchAsForm(two_fa_form, formData);

      if (response.status == 200) {
        if (auth_select.value == 'APP') {
          try {
            const json = await response.json();
            const qr = json['qr'];
            const qr_element = document.getElementById('app_qr');
            const app_url = document.getElementById('app-url');
            const app_auth_url = document.getElementById('app-auth-url');

            qr_element.src = 'data:image/png;base64,' + qr;
            app_url.value = json['app_url'];
            app_auth_url.value = json['app_url'];

            qr_element.hidden = false;
          } catch {
            document.getElementById('server-error').hidden = false;
          }
        }
        switchingTwoFA(true);
      } else {
        document.getElementById('server-error').hidden = false;
      }
    }
    */
  });
  phone_input.addEventListener('input', function () {
    phone_auth_error.hidden = true;
  });

  /*
  const back_button = document.getElementById('back-button');
  back_button.addEventListener('click', function () {
    switchingTwoFA(false);
  });
  */
  two_fa_button.addEventListener('click', async function (event) {
    event.preventDefault();
    const form = document.getElementById('two-fa-form');
    const failure_verify_2fa = document.getElementById('failure-verify-2fa');
    failure_verify_2fa.hidden = true;
    const formData = new FormData(form);
    const response = await fetchAsForm(form, formData);

    if (response.status == 200) {
      signup_form.action = '/accounts/signup/';

      const signup_form_elements = signup_form.querySelectorAll('input,radio,select, button');
      signup_form_elements.forEach((element) => {
        element.disabled = false;
      });

      const formData = new FormData(signup_form);
      const response = await fetchAsForm(signup_form, formData);
      if (response.status == 200) {
        document.querySelector('#app').innerHTML = await response.text();
      } else {
        failure_verify_2fa.hidden = false;
      }
    } else {
      failure_verify_2fa.hidden = false;
    }
  });

  const verify_code = document.getElementById('verify-code');
  verify_code.addEventListener('input', function () {
    const failure_verify_2fa = document.getElementById('failure-verify-2fa');
    failure_verify_2fa.hidden = true;
  });
});
