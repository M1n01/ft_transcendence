import Point from './Point.js';

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
    let x = this.point.x - width;
    let y = this.prePoint.y;

    this.div.style.top = `${y}px`;
    this.div.style.left = `${x}px`;
    this.div.style.width = `${width * 2}px`;
    this.div.style.height = '1px';
    this.div.classList.add('tournamentLine');
    parent.appendChild(this.div);
  }
  draw_seed(parent) {
    let x = this.point.x;
    let y = this.prePoint.y;
    const width = Math.abs(this.offset.x);
    if (this.position == 'left') {
      x = x - width;
    }

    this.div.style.top = `${y}px`;
    this.div.style.left = `${x}px`;
    this.div.style.width = `${width}px`;
    this.div.style.height = '1px';
    this.div.classList.add('tournamentLine');
    parent.appendChild(this.div);
  }

  draw_normal(parent) {
    const bottom = document.createElement('div');
    if (this.position == 'left') {
      const width = Math.abs(this.offset.x);
      const height = Math.abs(this.offset.y) * 2;
      const x = this.point.x + this.offset.x;
      const y = this.point.y - this.offset.y;

      this.div.style.top = `${y}px`;
      this.div.style.left = `${x}px`;
      this.div.style.width = `${width}px`;
      this.div.style.height = `${height}px`;
      this.div.classList.add('tournamentTopLeftBranch');

      bottom.style.top = `${y + this.offset.y * 2}px`;
      bottom.style.left = `${x}px`;
      bottom.style.width = `${width}px`;
      bottom.classList.add('tournamentBottomBranch');
    } else {
      const width = Math.abs(this.offset.x);
      const height = Math.abs(this.offset.y) * 2;
      const x = this.point.x; // + this.offset.x;
      const y = this.point.y - this.offset.y;

      this.div.style.top = `${y}px`;
      this.div.style.left = `${x}px`;
      this.div.style.width = `${width}px`;
      this.div.style.height = `${height}px`;
      this.div.classList.add('tournamentTopRightBranch');
      //this.div.classList.add('tournamentTopLeftBranch');

      bottom.style.top = `${y + this.offset.y * 2}px`;
      bottom.style.left = `${x}px`;
      bottom.style.width = `${width}px`;
      bottom.classList.add('tournamentBottomBranch');
    }
    parent.appendChild(this.div);
    parent.appendChild(bottom);
  }

  draw(parent) {
    if (this.id == 0) {
      //決勝戦
      this.draw_final(parent);
    } else if (this.seed_flag == true) {
      this.draw_seed(parent);
    } else {
      this.draw_normal(parent);
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

    const point1 = this.point.copyOffset(new Point(0, this.offset.y));
    const point2 = this.point.copyOffset(new Point(0, -this.offset.y));

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
