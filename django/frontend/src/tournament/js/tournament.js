//import { TournmentChartEvent } from './tournament_chart.js';
import { fetchAsForm } from '../../spa/js/utility/fetch.js';
import '../scss/tournament.scss';
import { router } from '../../spa/js/routing/routing.js';
import { reload, loadNav } from '../../spa/js/utility/user.js';
import { getDisplayedURI } from '../../../src/index.js';
//import { getDisplayedURI } from '../../../src/index.js';

export const TournmentEvent = new Event('TournmentEvent');

document.addEventListener('TournmentEvent', () => {
  const links = () => {
    console.log('links No.2');
    const links = document.querySelectorAll('a');
    links.forEach((event) => {
      console.log('links No.3');
      event.addEventListener('click', async (e) => {
        e.preventDefault();
        if (e.disabled == true) {
          //なぜか２回以上実行される
          //ここで無効化させる。
          return;
        }
        e.disabled = true;
        history.replaceState(null, null, event.href);
        await loadNav();

        const uri = getDisplayedURI(window.location.pathname);
        router(uri.rest, uri.params);
        console.log('links No.4');
        //console.log('event.href=' + event.href);
        //const uri = getDisplayedURI(event.href).path;
        //await moveTo(event.href);

        console.log('links No.5');
        e.disabled = false;

        //const data = fetchData(event.href);

        //document.querySelector('#app').innerHTML = html;
      });
      //document.querySelector('#app').innerHTML = html;
    });
  };

  const top = () => {
    console.log('top No.1');
    const register_tournaments = document.querySelectorAll('.register-tournament');
    const close_register_modal = document.getElementById('close-register-modal');

    console.log('top No.2');
    if (register_tournaments == null) {
      console.log('top No.3');
      return;
    }

    console.log('top No.4');
    register_tournaments.forEach((element) => {
      console.log('top No.5');
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

    console.log('top No.6');
    document.getElementById('make-tournment').addEventListener('submit', async function (event) {
      console.log('top No.7');
      event.preventDefault();
      const form = event.target;
      const formData = new FormData(form);
      const response = await fetchAsForm(form, formData);
      if (response.status != 200) {
        console.error('filure to post form. Status:' + response.status);
        return;
      }
      console.log('top No.8');
      await reload();
    });
    console.log('top No.9');
  };

  try {
    console.log('links No.1');
    console.log('links No.1');
    console.log('links No.1');
    console.log('links No.1');
    links();
  } catch {
    return;
  }
  console.log('TournmentEvent No.1');
  try {
    console.log('TournmentEvent No.2');
    top();
    console.log('TournmentEvent No.3');
  } catch {
    console.log('TournmentEvent No.4');
    return;
  }
});
