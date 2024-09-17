//import { TournmentChartEvent } from './tournament_chart.js';
import { fetchAsForm } from '../../spa/js/utility/fetch.js';
import '../scss/tournament.scss';

export const TournmentEvent = new Event('TournmentEvent');
document.addEventListener('TournmentEvent', () => {
  document.getElementById('make-tournment').addEventListener('submit', async function (event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const response = await fetchAsForm(form, formData);
    if (response.status != 200) {
      return;
    }

    //document.dispatchEvent(RebuildTournmentEvent);
    //document.dispatchEvent(TournmentChartEvent);
  });
});
