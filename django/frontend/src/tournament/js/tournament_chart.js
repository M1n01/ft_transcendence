//import TournamentChart from './tournament/TournamentChart.js';
import TournamentChart from './tournament/TournamentChart.js';
import '../scss/tournament.scss';

export const TournamentChartEvent = new Event('TournamentChartEvent');
document.addEventListener('TournamentChartEvent', () => {
  try {
    const chart_div = document.getElementById('chart-div'); // 既存の要素を取得
    //const player_count_element = document.getElemetnByid('current_players');
    const player_count = Number(document.getElementById('id_current_players').value);
    const tournament = document.getElementById('tournament-div'); // 既存の要素を取得
    chart_div.hidden = false;

    /*
  const newDiv = document.createElement('div');
  const width = 500;
  newDiv.classList.add('tournamentLine');
  newDiv.style.width = `${width}px`;
  newDiv.style.height = '200px';
  newDiv.style.top = '30px';
  newDiv.style.left = '0px';
  tournament.appendChild(newDiv);
  */

    //const = document.getElementById('tournament-canvas');
    const totalParticipants = player_count;

    const chart = new TournamentChart(tournament, totalParticipants);
    chart.init();

    const tmp_users = [
      'test1ABCDEFGHIJKLMN',
      'ABCDEFGHIJKLMN',
      'test3',
      'test4',
      'test5',
      'test6',
      'test7',
      'test8',
      'test9',
      'test10',
      'testA1',
      'testA2',
      'testA3',
      'testA4',
      'testA5',
      'testA6',
      'testA7',
      'testA8',
      'testA9',
      'testA10',
      'testB1',
      'testB2',
      'testB3',
      'testB4',
      'testB5',
      'testB6',
      'testB7',
      'testB8',
      'testB8',
      'testB8',
      'testB8',
      'testB8',
      'testB8',
      'testB8',
      'testB8',
      'testB8',
      'testB8',
      'testB8',
      'testB8',
      'testB8',
    ];

    const users = [];
    for (let i = 0; i < player_count; i++) {
      users.push(tmp_users[i]);
    }

    if (chart.setParticipants(users) == false) {
      console.log('user set error');
      return false;
    }
    chart.draw();
    chart.drawParticipants();
  } catch {
    return;
  }
});
