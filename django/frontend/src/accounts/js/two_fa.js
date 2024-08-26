import { fetchAsForm } from '../../spa/js/utility/fetch.js';
import '../scss/two_fa.scss';
export const TwoFaEvent = new Event('TwoFaEvent');

document.addEventListener('TwoFaEvent', function () {
  const two_fa_form = document.getElementById('two-fa-verify-form');
  const input_code = document.getElementById('two-fa-verify-code');
  const error_message = document.getElementById('failure-verify');
  const resend_error = document.getElementById('failure-resend');
  const resend_two_fa = document.getElementById('resend-two-fa');

  two_fa_form.addEventListener('submit', async function (event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const response = await fetchAsForm(form, formData);
    if (response.status != 200) {
      error_message.hidden = false;
    }
  });
  input_code.addEventListener('input', () => {
    error_message.hidden = true;
    resend_error.hidden = true;
  });

  resend_two_fa.addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const response = await fetchAsForm(form, formData);
    if (response.status == 200) {
      try {
        const json = await response.json();
        if (json['app']) {
          console.log('renew qr');
          document.getElementById('app_url_qr').src = 'data:image/png;base64,' + json['qr'];
        }
      } catch (e) {
        console.error(e);
      }
    } else {
      resend_error.hidden = false;
    }
  });
});
