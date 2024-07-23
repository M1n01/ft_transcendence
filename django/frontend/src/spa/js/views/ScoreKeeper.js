import AbstractView from './AbstractView.js';

export default class extends AbstractView {
  async getHtml() {
    return `
    <body>
      <h1>Score Keeper</h1>
      <form id="scoreForm">
          <label for="user_address">User Address:</label>
          <input type="text" id="user_address" name="user_address">
          <label for="score">Score:</label>
          <input type="number" id="score" name="score">
          <button type="button" onclick="setScore()">Set Score</button>
      </form>

      <script>
          async function setScore() {
              const user_address = document.getElementById('user_address').value;
              const score = document.getElementById('score').value;

              const response = await fetch('/api/scores/set_score/', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                  },
                  body: JSON.stringify({ user_address, score }),
              });

              const result = await response.json();
              console.log(result);
          }
      </script>
    </body>
    `;
  }
}
