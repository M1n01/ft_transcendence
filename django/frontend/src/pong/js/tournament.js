import { TournmentChartEvent } from './tournament_chart.js';
import '../scss/tournament.scss';

export const TournmentEvent = new Event('TournmentEvent');
document.addEventListener('TournmentEvent', () => {
  document.getElementById('make-tournment').addEventListener('submit', async function (event) {
    event.preventDefault();
    //document.dispatchEvent(RebuildTournmentEvent);
    document.dispatchEvent(TournmentChartEvent);
  });
});
