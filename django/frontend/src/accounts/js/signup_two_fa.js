import { fetchAsForm } from '../../spa/js/utility/fetch.js';
export const SignupTwoFAEvent = new Event('SignupTwoFAEvent');

document.addEventListener('SignupTwoFAEvent', function () {
  const two_fa_form = document.getElementById('two-fa-form');
  const input_code = document.getElementById('verify-code');
  const error_message = document.getElementById('failure-verify');
  const resend_form = document.getElementById('resend-form');
  const send_error = document.getElementById('failure-send');
  //const send_error = resend_form;

  two_fa_form.addEventListener('submit', async function (e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    let response = await fetchAsForm(form, formData);
    if (response.status == 200) {
      console.log('OK');
    } else {
      error_message.hidden = false;
      console.log('NG');
    }
    //const json = await response.json();
  });

  resend_form.addEventListener('submit', async function (e) {
    send_error.hidden = true;
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    const response = await fetchAsForm(form, formData);
    if (response.status == 200) {
      console.log('OK');
    } else {
      send_error.hidden = false;
      console.log('NG');
    }
  });

  input_code.addEventListener('input', () => {
    error_message.hidden = true;
    send_error.hidden = true;
  });
});
