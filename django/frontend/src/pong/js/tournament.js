//import TournmentChart from './tournament/TournamentChart.js';
import TournmentChart from './tournament/TournamentChart.js';
import '../scss/tournament.scss';

export const TournmentEvent = new Event('TournmentEvent');
document.addEventListener('TournmentEvent', () => {
  const tournment = document.getElementById('tournment-div'); // 既存の要素を取得

  /*
  const newDiv = document.createElement('div');
  const width = 500;
  newDiv.classList.add('tournamentLine');
  newDiv.style.width = `${width}px`;
  newDiv.style.height = '200px';
  newDiv.style.top = '30px';
  newDiv.style.left = '0px';
  tournment.appendChild(newDiv);
  */

  //const = document.getElementById('tournment-canvas');
  const totalParticipants = 6;

  const chart = new TournmentChart(tournment, totalParticipants);
  chart.init();

  const users = [
    'test1ABCDEFGHIJKLMN',
    'ABCDEFGHIJKLMN',
    'test3',
    'test4',
    'test5',
    'test6',
    //'test7',
    //'test8',
    //'test9',
    //'test10',
    //'testA1',
    //'testA2',
    //'testA3',
    //'testA4',
    //'testA5',
    //'testA6',
    //'testA7',
    //'testA8',
    //'testA9',
    //'testA10',
    //'testB1',
    //'testB2',
    //  'testB3',
    //  'testB4',
    //  'testB5',
    //  'testB6',
    //  'testB7',
    //  'testB8',
    //  'testB8',
    //  'testB8',
    //  'testB8',
    //  'testB8',
    //  'testB8',
    //  'testB8',
    //  'testB8',
    //  'testB8',
    //  'testB8',
    //  'testB8',
    //  'testB8',
    //  'testB8',
  ];

  if (chart.setParticipants(users) == false) {
    console.log('user set error');
    return false;
  }
  chart.draw();
  chart.drawParticipants();
});
