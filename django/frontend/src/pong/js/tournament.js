import TournmentChart from './tournament/TournamentChart.js';

export const TournmentEvent = new Event('TournmentEvent');
document.addEventListener('TournmentEvent', () => {
  const canvas = document.getElementById('tournment-canvas');
  const totalParticipants = 40;
  const chart = new TournmentChart(canvas, totalParticipants);
  chart.init();
  chart.draw();

  const users = [
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

  if (chart.setParticipants(users) == false) {
    console.log('user set error');
    return false;
  }
  chart.drawParticipants();
});
