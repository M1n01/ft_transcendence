import { fetchAsForm } from '../../spa/js/utility/fetch.js';
import '../scss/tournament.scss';
import { reload } from '../../spa/js/utility/user.js';

export const TournamentEvent = new Event('TournamentEvent');

document.addEventListener('TournamentEvent', () => {
  const links = () => {
    const links = document.querySelector('#app').querySelectorAll('a');
    links.forEach((event) => {
      event.dataset.link = '';
    });
  };

  const top_list = () => {
    const pre_register_tournaments = document.querySelectorAll('.open-register-tournament-modal');
    const register_tournament = document.getElementById('register-tournament');

    if (register_tournament == null) {
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

    //register_tournaments.forEach((element) => {
    register_tournament.addEventListener('submit', async (event) => {
      event.preventDefault();
      const form = event.target;
      const formData = new FormData(form);
      const response = await fetchAsForm(form, formData);
      const close_register_modal = document.getElementById('close-register-modal');
      const error_text = document.getElementById('register-limit-error');
      const error_text2 = document.getElementById('register-registered-ierror');
      if (response.status != 200) {
        const json = await response.json();
        if (json['is_full']) {
          error_text.hidden = false;
        } else if (json['is_registered']) {
          error_text2.hidden = false;
        }
        return;
      }
      close_register_modal.click();
      await reload();
    });
  };

  const top = () => {
    const making_tournament = document.getElementById('make-tournament');

    if (making_tournament == null) {
      return;
    }
    const close_modal = document.getElementById('create-tournament-cancel');
    const error_message = document.getElementById('make-tournament-error');
    error_message.hidden = true;

    // トーナメント新規作成
    making_tournament.addEventListener('submit', async function (event) {
      error_message.hidden = true;
      event.preventDefault();
      const form = event.target;
      const formData = new FormData(form);
      const response = await fetchAsForm(form, formData);
      if (response.status != 200) {
        error_message.hidden = false;
        console.error('filure to post form. Status:' + response.status);
        return;
      }
      close_modal.click();
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
    top_list();
  } catch {
    return;
  }
});
