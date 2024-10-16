import { submitForm } from '../../spa/js/utility/form.js';
import '../scss/two_fa.scss';
import { moveTo } from '../../spa/js/routing/routing.js';
import { Modal } from 'bootstrap';
import { WebsocketInit } from '../../spa/js/ws/socket.js';
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
  const cancel_two_fa = document.getElementById('cancel-two-fa');

  two_fa_form.addEventListener('submit', async function (event) {
    const response = await submitForm(event);
    input_code.value = '';
    if (response.status != 200) {
      error_message.hidden = false;
      return;
    }
    navModal(false);
    await moveTo('games');
    WebsocketInit();
  });

  cancel_two_fa.addEventListener('submit', async (event) => {
    const response = await submitForm(event);
    if (response.status != 200) {
      console.error('Error:cancel TwoFa');
      return;
    }
  });

  input_code.addEventListener('input', () => {
    error_message.hidden = true;
  });
});
