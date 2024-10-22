//import TournamentChart from './tournament/TournamentChart.js';
import TournamentChart from './tournament/TournamentChart.js';
import '../scss/tournament.scss';
//import { fetchJsonData } from '../../spa/utility/fetch.js';
import { fetchJsonData } from '../../spa/js/utility/fetch.js';

export const RebuildTournamentEvent = new Event('RebuildTournamentEvent');

document.addEventListener('RebuildTournamentEvent', async () => {
  const chart_element = document.getElementById('tournament-chart');
  if (!chart_element) {
    return;
  }
  const id = document.getElementById('id-hidden');
  const url = '/tournament/info/' + id.value;
  const json = await fetchJsonData(url);
  const tournament = document.getElementById('tournament-div'); // 既存の要素を取得
  const totalParticipants = json['max_user_cnt'];

  const chart = new TournamentChart(tournament, totalParticipants);
  chart.init();

  const matches = json['matches'];

  if (chart.setGames(matches) == false) {
    return false;
  }
  chart.draw();
  chart.drawParticipants();
});
