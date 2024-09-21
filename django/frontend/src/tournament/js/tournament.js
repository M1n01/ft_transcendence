import { fetchAsForm } from '../../spa/js/utility/fetch.js';
import '../scss/tournament.scss';
import { reload } from '../../spa/js/utility/user.js';

export const TournmentEvent = new Event('TournmentEvent');

document.addEventListener('TournmentEvent', () => {
  const links = () => {
    const links = document.querySelector('#app').querySelectorAll('a');
    console.log('links.size=' + links.length);
    links.forEach((event) => {
      event.dataset.link = '';
    });
  };

  const top = () => {
    const register_tournaments = document.querySelectorAll('.register-tournament');
    const close_register_modal = document.getElementById('close-register-modal');

    if (register_tournaments == null) {
      return;
    }

    register_tournaments.forEach((element) => {
      element.addEventListener('submit', async (event) => {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        const response = await fetchAsForm(form, formData);
        if (response.status != 200) {
          console.error('filure to post form. Status:' + response.status);
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
