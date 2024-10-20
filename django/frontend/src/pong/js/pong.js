import { submitForm } from '../../spa/js/utility/form.js';
import { moveTo } from '../../spa/js/routing/routing.js';
//import { PongMainEvent } from './pong/main.js';
export const GameEvent = new Event('GameEvent');

document.addEventListener('GameEvent', function () {
  console.log('GameEvent No.1');
  //document.dispatchEvent(PongMainEvent);

  const test_game = document.getElementById('start-test-game');
  if (test_game == null) {
    console.log();
    return;
  }
  console.log('GameEvent No.2');

  const tournament_game = document.getElementById('start-tournament-game');

  const error_message_test = document.getElementById('error-game');
  error_message_test.hidden = true;

  const error_message_tournament = document.getElementById('error-no-tournament');
  error_message_tournament.hidden = true;

  test_game.addEventListener('submit', async (event) => {
    //event.preventDefault();
    const response = await submitForm(event);
    if (response.error) {
      error_message_test.hidden = false;
      return;
    }
    const json = await response.json();
    try {
      //const url = 'pong/match/' + json['id'];
      //console.log('url:' + url);
      moveTo(`/pong/match/${json['id']}`);
    } catch {
      error_message_test.hidden = false;
      console.error('Error:start pong');
      return;
    }
  });

  tournament_game.addEventListener('submit', async (event) => {
    const response = await submitForm(event);
    if (response.error) {
      error_message_tournament.hidden = false;
      return;
    }
    const json = await response.json();
    try {
      //const url = 'pong/match/' + json['id'];
      //console.log('url:' + url);
      moveTo(`/pong/match/${json['id']}`);
    } catch {
      error_message_tournament.hidden = false;
      console.error('Error:start pong');
      return;
    }
  });
});
