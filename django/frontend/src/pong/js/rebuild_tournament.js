//import TournmentChart from './tournament/TournamentChart.js';
import TournmentChart from './tournament/TournamentChart.js';
import '../scss/tournament.scss';

export const RebuildTournmentEvent = new Event('RebuildTournmentEvent');
document.addEventListener('RebuildTournmentEvent', () => {
  const tournment = document.getElementById('tournment-div'); // 既存の要素を取得

  const totalParticipants = 6;

  const chart = new TournmentChart(tournment, totalParticipants);
  chart.init();

  const games = [
    {
      id: 12,
      winner: 'test1',
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

  if (chart.setGames(games) == false) {
    console.log('user set error');
    return false;
  }
  chart.draw();
  chart.drawParticipants();
});
