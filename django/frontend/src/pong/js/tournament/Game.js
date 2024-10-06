//import { RedirectHandler } from '../../../../../../../../../../.cache/typescript/5.5/node_modules/undici-types/handlers.js';
import Point from './Point.js';
import crown_img from '../../assets//medal-crown-10328-gold.png';

export default class Game {
  constructor(point, offset, edge_flag, id, position, pre_point) {
    this.point = point;
    this.prePoint = pre_point;
    this.offset = offset;

    if (edge_flag == undefined) {
      this.edge_flag = false;
    } else {
      this.edge_flag = edge_flag;
    }
    this.seed_flag = false;
    this.id = id;
    this.user1 = null;
    this.user2 = null;
    this.position = position;
    this.winner = null;

    this.div = document.createElement('div');
  }

  draw_final(parent) {
    const width = Math.abs(this.offset.x);
    ///const height = Math.abs(this.offset.y);
    let x = this.point.x - width;
    let y = this.prePoint.y - 3;

    //bottom.style.top = `${y + this.offset.y * 2}px`;
    this.div.style.top = `${y}px`;
    this.div.style.left = `${x}px`;
    this.div.style.width = `${width * 2}px`;
    this.div.style.height = '1px';
    this.div.classList.add('tournamentLine');
    parent.appendChild(this.div);

    if (this.winner != null) {
      const circle = document.createElement('div');
      circle.style.top = `${this.point.y - 7}px`;
      circle.style.left = `${this.point.x - 9}px`;
      circle.classList.add('gameCircle');
      parent.appendChild(circle);

      const winnerTop = document.createElement('div');
      const winner_image = document.createElement('img');
      //winner_image.src = 'static/asset/pong/medal-crown-10328-gold.png';
      winner_image.src = crown_img;
      winner_image.classList.add('w-100');

      winnerTop.style.bottom = `${y + width}px`;
      winnerTop.style.left = `${x + (width * 0.5) / 2 + 1}px`;
      winnerTop.style.width = `${width * 1.5}px`;
      winnerTop.style.height = `${width * 1.5}px`;
      //winnerTop.classList.add('winner');
      winnerTop.style.position = 'absolute';
      //winnerTop.classList.add('validRight');
      winnerTop.appendChild(winner_image);

      const winner = document.createElement('div');
      winner.style.top = `${y}px`;
      winner.style.width = `${width + 2}px`;
      winner.classList.add('winner');
      winner.classList.add('validTop');
      winner.style.height = '1px';

      if (this.winner == this.user1) {
        winner.style.left = `${x - 2}px`;
      } else {
        winner.style.left = `${x + width - 2}px`;
      }
      parent.appendChild(winner);
      parent.appendChild(winnerTop);
    }
  }
  draw_seed(parent, next_game) {
    let x = this.point.x;
    let y = this.prePoint.y;
    const width = Math.abs(this.offset.x);
    if (this.position == 'left') {
      x = x - width;
    }

    this.div.style.top = `${y}px`;
    this.div.style.left = `${x}px`;
    this.div.style.width = `${width}px`;
    this.div.style.height = '0px';

    // 次の試合で勝った時だけ赤くする
    if (this.winner != null && next_game.winner == this.winner) {
      this.div.classList.add('winner');
      this.div.classList.add('validTop');
    } else {
      this.div.classList.add('tournamentLine');
    }
    //this.div.classList.add('winnerLeft');
    parent.appendChild(this.div);
  }

  draw_right_winner(parent, x, y, width, height, next_game) {
    const winnerTop = document.createElement('div');
    const winnerBottom = document.createElement('div');
    const winnerLeft = document.createElement('div');

    winnerTop.style.top = `${y}px`;
    winnerTop.style.left = `${x}px`;
    winnerTop.style.width = `${width}px`;
    winnerTop.style.height = `${height}px`;
    winnerTop.classList.add('winner');
    winnerTop.classList.add('validTop');

    winnerBottom.style.top = `${y + this.offset.y * 2}px`;
    winnerBottom.style.left = `${x}px`;
    winnerBottom.style.width = `${width}px`;
    winnerBottom.style.height = `${height}px`;
    winnerBottom.classList.add('winner');
    winnerBottom.classList.add('validTop');

    winnerLeft.style.top = `${y}px`;
    winnerLeft.style.left = `${x}px`;
    winnerLeft.style.width = `${width}px`;
    winnerLeft.style.height = `${height}px`;
    winnerLeft.classList.add('winner');
    winnerLeft.classList.add('validLeft');

    if (this.winner == this.user1) {
      winnerTop.style.width = `${width}px`;
      winnerLeft.style.top = `${y}px`;
      winnerBottom.style.left = `${x + width / 2}px`;
      winnerBottom.style.width = `${width / 2}px`;

      parent.appendChild(winnerTop);
      if (this.edge_flag == false && next_game && next_game.seed_flag == false) {
        parent.appendChild(winnerBottom);
      }
    } else {
      winnerTop.style.left = `${x + width / 2}px`;
      winnerTop.style.width = `${width / 2}px`;
      winnerLeft.style.top = `${y + height}px`;
      winnerBottom.style.width = `${width}px`;
      parent.appendChild(winnerBottom);
      if (this.edge_flag == false && next_game && next_game.seed_flag == false) {
        parent.appendChild(winnerTop);
      }
    }
    parent.appendChild(winnerLeft);
  }
  draw_left_winner(parent, x, y, width, height, next_game) {
    const winnerTop = document.createElement('div');
    const winnerBottom = document.createElement('div');
    const winnerRight = document.createElement('div');

    winnerTop.style.top = `${y}px`;
    winnerTop.style.left = `${x}px`;
    winnerTop.style.width = `${width}px`;
    winnerTop.style.height = `${height}px`;
    winnerTop.classList.add('winner');
    winnerTop.classList.add('validTop');

    winnerBottom.style.top = `${y + this.offset.y * 2}px`;
    winnerBottom.style.left = `${x}px`;
    winnerBottom.style.width = `${width}px`;
    winnerBottom.style.height = `${height}px`;
    winnerBottom.classList.add('winner');
    winnerBottom.classList.add('validTop');

    winnerRight.style.top = `${y}px`;
    winnerRight.style.left = `${x}px`;
    winnerRight.style.width = `${width}px`;
    winnerRight.style.height = `${height}px`;
    winnerRight.classList.add('winner');
    winnerRight.classList.add('validRight');

    if (this.winner == this.user1) {
      winnerTop.style.width = `${width}px`;
      winnerRight.style.top = `${y}px`;
      winnerBottom.style.width = `${width / 2}px`;

      parent.appendChild(winnerTop);
      if (this.edge_flag == false && next_game && next_game.seed_flag == false) {
        parent.appendChild(winnerBottom);
      }
    } else {
      winnerTop.style.width = `${width / 2}px`;
      winnerRight.style.top = `${y + height}px`;
      winnerBottom.style.width = `${width}px`;
      parent.appendChild(winnerBottom);
      if (this.edge_flag == false && next_game && next_game.seed_flag == false) {
        parent.appendChild(winnerTop);
      }
    }
    parent.appendChild(winnerRight);
  }

  draw_normal(parent, next_game) {
    const bottom = document.createElement('div');

    if (this.position == 'left') {
      const width = Math.abs(this.offset.x);
      const height = Math.abs(this.offset.y);
      const x = this.point.x + this.offset.x;
      const y = this.point.y - this.offset.y;

      this.div.style.top = `${y}px`;
      this.div.style.left = `${x}px`;
      this.div.style.width = `${width}px`;
      this.div.style.height = `${height * 2}px`;
      this.div.classList.add('tournamentTopLeftBranch');

      bottom.style.top = `${y + this.offset.y * 2}px`;
      bottom.style.left = `${x}px`;
      bottom.style.width = `${width}px`;
      bottom.classList.add('tournamentBottomBranch');

      if (this.winner != null) {
        const circle = document.createElement('div');
        circle.style.top = `${this.point.y - 7}px`;
        circle.style.left = `${this.point.x - 9}px`;
        circle.classList.add('gameCircle');
        parent.appendChild(circle);

        this.draw_left_winner(parent, x, y, width, height, next_game);
      }
    } else {
      // right
      const width = Math.abs(this.offset.x);
      const height = Math.abs(this.offset.y);
      const x = this.point.x;
      const y = this.point.y - this.offset.y;

      this.div.style.top = `${y}px`;
      this.div.style.left = `${x}px`;
      this.div.style.width = `${width}px`;
      this.div.style.height = `${height * 2}px`;
      this.div.classList.add('tournamentTopRightBranch');
      //this.div.classList.add('tournamentTopLeftBranch');

      bottom.style.top = `${y + this.offset.y * 2}px`;
      bottom.style.left = `${x}px`;
      bottom.style.width = `${width}px`;
      bottom.classList.add('tournamentBottomBranch');

      if (this.winner != null) {
        const circle = document.createElement('div');
        circle.style.top = `${this.point.y - 7}px`;
        circle.style.left = `${this.point.x - 5}px`;
        circle.classList.add('gameCircle');
        parent.appendChild(circle);
        this.draw_right_winner(parent, x, y, width, height, next_game);
      }
    }
    parent.appendChild(this.div);
    parent.appendChild(bottom);
  }

  draw(parent, next_game) {
    if (this.id == 0) {
      //決勝戦
      this.draw_final(parent);
    } else if (this.seed_flag == true) {
      this.draw_seed(parent, next_game);
    } else {
      this.draw_normal(parent, next_game);
    }
  }
  getNewGames(edge_flag) {
    const y = this.point.y - this.offset.y;

    //const seed_point1 = new Point(0, this.point.y + this.offset.y - 3 + (this.offset.y % 2) * 200);
    const seed_point1 = new Point(0, y);
    const seed_point2 = new Point(0, y + this.offset.y * 2);
    const new_game1 = new Game(
      new Point(this.point.x + this.offset.x, this.point.y - this.offset.y),
      //new Point(this.offset.x, parseInt(this.offset.y / 2) + 1 + (this.offset.y % 2)), // +1がないとずれる
      new Point(this.offset.x, parseInt(this.offset.y / 2)), // +1がないとずれる
      edge_flag,
      this.id * 10 + 1,
      this.position,
      seed_point1
    );
    const new_game2 = new Game(
      new Point(this.point.x + this.offset.x, this.point.y + this.offset.y + 3),
      //new Point(this.offset.x, parseInt(this.offset.y / 2) + (this.offset.y % 2)),
      new Point(this.offset.x, parseInt(this.offset.y / 2)),
      edge_flag,
      this.id * 10 + 2,
      this.position,
      seed_point2
    );
    return [new_game1, new_game2];
  }

  appendUserText(user, parent, point, width, height) {
    const text = document.createElement('div');
    text.style.top = `${point.y}px`;
    text.style.left = `${point.x}px`;
    text.style.width = `${width}px`;
    text.style.height = `${height}px`;
    if (this.position == 'left') {
      text.style.textAlign = 'right';
    } else {
      text.style.textAlign = 'left';
    }
    text.classList.add('userTextArea');
    text.textContent = user;
    //text.textContent = this.id;
    parent.appendChild(text);
  }

  drawSeedUser(parent) {
    let tmp_offset;
    const height = Math.abs(this.offset.y) * 1.5;
    const width = Math.abs(this.offset.x) * 2.5;

    if (this.position == 'left') {
      tmp_offset = new Point(-width * 1.5 - 10, -height / 2);
    } else {
      tmp_offset = new Point(Math.abs(this.offset.x) + 10, -height / 2);
    }
    const text_point = this.point.copyOffset(tmp_offset);

    this.appendUserText(this.user1, parent, text_point, width, height);
  }
  drawNotSeedUser(parent) {
    //const tmp_point = new Point(this.offset.x, -this.offset.y);

    let tmp_offset;
    const height = Math.abs(this.offset.y) * 1.5;
    const width = Math.abs(this.offset.x) * 2.5;

    //const offset1 = New Point();

    const point1 = this.point.copyOffset(new Point(0, -this.offset.y));
    const point2 = this.point.copyOffset(new Point(0, this.offset.y));

    if (this.position == 'left') {
      tmp_offset = new Point(-width * 1.5 - 10, -height / 2);
    } else {
      tmp_offset = new Point(Math.abs(this.offset.x) + 10, -height / 2);
    }

    const user1_point = point1.copyOffset(tmp_offset);
    const user2_point = point2.copyOffset(tmp_offset);

    this.appendUserText(this.user1, parent, user1_point, width, height);
    this.appendUserText(this.user2, parent, user2_point, width, height);
  }

  drawUser(parent) {
    if (this.seed_flag) {
      this.drawSeedUser(parent);
    } else {
      this.drawNotSeedUser(parent);
    }
  }

  setUser(user1, user2) {
    this.user1 = user1;
    if (this.seed_flag == false) {
      this.user2 = user2;
    }
  }
  setSeed(flag) {
    this.seed_flag = flag;
  }
}
