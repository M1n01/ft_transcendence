import '../scss/signup.scss';
import { fetchAsForm } from '../../spa/js/utility/fetch.js';
import { TwoFaEvent } from './two_fa.js';
import { navModal } from './two_fa.js';
import { getUrlWithLang } from '../../spa/js/utility/url.js';
export const SignupEvent = new Event('SignupEvent');

function SetTime() {
  const Mytoday = new Date();
  const yyyy = Mytoday.getFullYear();
  const mm = String(Mytoday.getMonth() + 1).padStart(2, '0');
  const dd = String(Mytoday.getDate()).padStart(2, '0');
  const todayString = `${yyyy}-${mm}-${dd}`;
  document.getElementById('id_created_at').value = todayString;
  document.getElementById('birth_date_id').type = 'date';
}

document.addEventListener('SignupEvent', function () {
  try {
    SetTime();

    const signup_form = document.getElementById('signup-form');
    const auth_select = document.getElementById('auth_id');
    const phone_input = document.getElementById('phone_id');
    const phone_auth_error = document.getElementById('phone-auth-error');
    signup_form.addEventListener('submit', async function (e) {
      e.preventDefault();
      const form = e.target;
      if (form.disabled == true) {
        return;
      }

      form.disabled = true;
      if (auth_select.value == 'SMS' && phone_input.value == '') {
        phone_auth_error.hidden = false;
        return;
      }
      const formData = new FormData(form);
      let response = await fetchAsForm(form, formData);
      form.disabled = false;

      if (response.status == 200) {
        try {
          const json = await response.json();
          if (json['valid'] == false) {
            const html = json['html'];
            document.querySelector('#signup-area').innerHTML = html;
            document.dispatchEvent(SignupEvent);
            return;
          }
          const two_fa_form = document.getElementById('two-fa-verify-form');
          const resend_two_fa_form = document.getElementById('resend-two-fa');
          two_fa_form.action = getUrlWithLang('accounts/signup-two-fa/');
          resend_two_fa_form.action = 'accounts/signup-two-fa/';
          if (json['is_auth_app']) {
            document.getElementById('app_url_qr').hidden = false;
            document.getElementById('app_url_qr').src = 'data:image/png;base64,' + json['qr'];
          } else {
            document.getElementById('app_url_qr').hidden = true;
          }

          navModal(true);
          document.dispatchEvent(TwoFaEvent);
          return;
        } catch (error) {
          console.error(error);
        }
      } else if (response.status == 400) {
        const html = await response.text();
        document.querySelector('#signup-area').innerHTML = html;
        document.dispatchEvent(SignupEvent);
      }
    });
    phone_input.addEventListener('input', function () {
      phone_auth_error.hidden = true;
    });

    const verify_code = document.getElementById('signup-verify-code');
    verify_code.addEventListener('input', function () {
      const failure_verify_2fa = document.getElementById('failure-verify-2fa');
      failure_verify_2fa.hidden = true;
    });
  } catch (error) {
    console.log('ignore error:' + error);
  }
});
