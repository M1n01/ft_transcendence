import { fetchAsForm } from '../../spa/js/utility/fetch.js';
import '../scss/two_fa.scss';
import { moveTo } from '../../spa/js/routing/routing.js';
import { Modal } from 'bootstrap';
export const TwoFaEvent = new Event('TwoFaEvent');

let modal = null;
export function navModal(open) {
  if (modal == null) {
    const modal_2fa = document.getElementById('TwoFa-Modal');
    modal = new Modal(modal_2fa);
  }

  if (open) {
    modal.show();
  } else {
    modal.hide();

    // nullを入れずに再利用しようとすると、
    // なぜか認証コードが空白で送られてしまうのnullを入れて新規に作り直す。
    modal = null;
  }
}

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
    input_code.value = '';
    if (response.status != 200) {
      error_message.hidden = false;
      return;
    }
    navModal(false);
    moveTo('games');
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
