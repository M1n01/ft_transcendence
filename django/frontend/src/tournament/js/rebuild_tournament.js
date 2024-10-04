//import TournmentChart from './tournament/TournamentChart.js';
import TournmentChart from './tournament/TournamentChart.js';
import '../scss/tournament.scss';
//import { fetchJsonData } from '../../spa/utility/fetch.js';
import { fetchJsonData } from '../../spa/js/utility/fetch.js';

export const RebuildTournmentEvent = new Event('RebuildTournmentEvent');

document.addEventListener('RebuildTournmentEvent', async () => {
  const chart_element = document.getElementById('tournament-chart');
  if (!chart_element) {
    return;
  }
  const id = document.getElementById('id-hidden');
  const url = '/tournament/info/' + id.value;
  const json = await fetchJsonData(url);
  const tournment = document.getElementById('tournment-div'); // 既存の要素を取得
  const totalParticipants = json['max_user_cnt'];

  const chart = new TournmentChart(tournment, totalParticipants);
  chart.init();

  const matches = json['matches'];
  /*
  for (let i = 0; i < matches.length; i++) {
    console.log(matches[i]);
  }
    */

  if (chart.setGames(matches) == false) {
    return false;
  }
  chart.draw();
  chart.drawParticipants();
});
