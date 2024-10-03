import { fetchAsForm } from '../../spa/js/utility/fetch.js';
import '../scss/tournament.scss';
import { reload } from '../../spa/js/utility/user.js';

export const TournmentEvent = new Event('TournmentEvent');

document.addEventListener('TournmentEvent', () => {
  const links = () => {
    const links = document.querySelector('#app').querySelectorAll('a');
    links.forEach((event) => {
      event.dataset.link = '';
    });
  };

  const top = () => {
    const pre_register_tournaments = document.querySelectorAll('.pre-register-tournament');
    const register_tournaments = document.querySelectorAll('.register-tournament');

    if (register_tournaments == null) {
      return;
    }

    pre_register_tournaments.forEach((button) => {
      button.addEventListener('click', (e) => {
        const target = e.target;
        const id_element = document.getElementById('retister-modal-id');
        const write_name = document.getElementById('register-tournament-name');
        id_element.value = target.value;
        write_name.textContent = target.name;
      });
    });

    register_tournaments.forEach((element) => {
      element.addEventListener('submit', async (event) => {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        const response = await fetchAsForm(form, formData);
        const close_register_modal = document.getElementById('close-register-modal');
        const error_text = document.getElementById('register-limit-error');
        if (response.status != 200) {
          const json = await response.json();
          if (json['is_full']) {
            error_text.hidden = false;
            close_register_modal.addEventListener('click', async () => {
              await reload();
            });
          }
          return;
        }
        close_register_modal.click();
        await reload();
      });
    });

    document.getElementById('make-tournment').addEventListener('submit', async function (event) {
      event.preventDefault();
      const form = event.target;
      const formData = new FormData(form);
      const response = await fetchAsForm(form, formData);
      if (response.status != 200) {
        console.error('filure to post form. Status:' + response.status);
        return;
      }
      await reload();
    });
  };

  try {
    links();
  } catch {
    return;
  }
  try {
    top();
  } catch {
    return;
  }
});
