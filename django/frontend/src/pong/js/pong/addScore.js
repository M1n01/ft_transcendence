import { fetchAsForm } from '../../../spa/js/utility/fetch.js';
import crown_img from '../../assets/medal-crown-10328-gold.png';

export const addScore = async (ball, area) => {
  console.log('addo score');
  const add_score_form = document.getElementById('add-score-game');
  const error_connect_message = document.getElementById('connection-error-message');

  if (ball.position.x <= area.minX) {
    console.log('add player2');
    add_score_form.elements['player1_score'].value = 0;
    add_score_form.elements['player2_score'].value = 1;
  } else {
    console.log('add player1');
    add_score_form.elements['player1_score'].value = 1;
    add_score_form.elements['player2_score'].value = 0;
  }

  const formData = new FormData(add_score_form);
  const response = await fetchAsForm(add_score_form, formData);
  if (response.error) {
    error_connect_message.hidden = false;
    return;
  }
  //await startPong();
  const json = await response.json();
  let score1 = json['player1_score'];
  let score2 = json['player2_score'];
  //let type = json['type'];
  const score_text1 = document.getElementById('player1_current_score');
  const score_text2 = document.getElementById('player2_current_score');
  const back_button = document.getElementById('back-button');
  //const next_game_type = document.getElementById('next-game-type');
  score_text1.textContent = score1;
  score_text2.textContent = score2;
  console.log('score_text1' + Number(score1));
  console.log('score_text2' + Number(score2));

  if (Number(score1) >= 5) {
    const player1_win = document.getElementById('player1-win');
    player1_win.src = crown_img;
    player1_win.hidden = false;
    back_button.hidden = false;
    //next_game_type.value = 'test';
  }
  if (Number(score2) >= 5) {
    const player2_win = document.getElementById('player2-win');
    player2_win.src = crown_img;
    player2_win.hidden = false;
    back_button.hidden = false;
  }
};
