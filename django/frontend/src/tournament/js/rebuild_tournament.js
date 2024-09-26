//import TournmentChart from './tournament/TournamentChart.js';
import TournmentChart from './tournament/TournamentChart.js';
import '../scss/tournament.scss';
//import { fetchJsonData } from '../../spa/utility/fetch.js';
import { fetchJsonData } from '../../spa/js/utility/fetch.js';

export const RebuildTournmentEvent = new Event('RebuildTournmentEvent');

document.addEventListener('RebuildTournmentEvent', async () => {
  const chart_element = document.getElementById('tournament-chart');
  if (!chart_element) {
    console.log('not tournament chart');
    return;
  }
  const id = document.getElementById('id-hidden');
  const url = '/tournament/info/' + id.value;
  console.log('url=' + url);
  const json = await fetchJsonData(url);
  console.log('json:' + json);

  const tournment = document.getElementById('tournment-div'); // 既存の要素を取得

  //const totalParticipants = 5;
  const totalParticipants = json['max_user_cnt'];
  console.log('totalParticipants=' + totalParticipants);

  const chart = new TournmentChart(tournment, totalParticipants);
  chart.init();

  const matches = json['matches'];
  for (let i = 0; i < matches.length; i++) {
    console.log(matches[i]);
  }
  /*
  const games = [
    {
      id: 12,
      winner: 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
      loser: '',
      winner_score: '3',
      loser_score: '2',
    },
    {
      id: 11,
      winner: 'test3',
      loser: 'test2',
      winner_score: '5',
      loser_score: '2',
    },
    {
      id: 21,
      winner: 'test4',
      loser: 'test5',
      winner_score: '4',
      loser_score: '3',
    },
    {
      id: 22,
      winner: 'test6',
      loser: '',
      winner_score: '6',
      loser_score: '1',
    },
    {
      id: 1,
      winner: 'test1',
      loser: 'test3',
      winner_score: '4',
      loser_score: '0',
    },
    {
      id: 2,
      winner: 'test6',
      loser: 'test4',
      winner_score: '7',
      loser_score: '3',
    },
    {
      id: 0,
      winner: 'test5',
      loser: 'test1',
      winner_score: '6',
      loser_score: '4',
    },
  ];
  */

  if (chart.setGames(matches) == false) {
    //if (chart.setGames(games) == false) {
    //console.log('user set error');
    return false;
  }
  chart.draw();
  chart.drawParticipants();
});
