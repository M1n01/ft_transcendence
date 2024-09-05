import Point from './Point.js';
import Line from './Line.js';

export default class Branch {
  constructor(line, offsetPoint, edge_flag, id) {
    //super(line.point());
    this.line = line;
    this.offset = offsetPoint;
    this.radius = 3.5;
    if (edge_flag == undefined) {
      this.edge_flag = false;
    } else {
      this.edge_flag = edge_flag;
    }
    this.seed_flag = false;
    this.id = id;
    this.user1 = null;
    this.user2 = null;
  }

  draw_seed(ctx) {
    ctx.beginPath();
    this.line.moveTo(ctx);
    this.line.lineToX(ctx, this.offset.x);
    ctx.stroke();
  }

  draw_normal(ctx) {
    ctx.beginPath();
    ctx.arc(this.line.x, this.line.y, this.radius, 0, Math.PI * 2);
    ctx.fill();

    this.line.moveTo(ctx);
    let new_line = this.line.lineToY(ctx, this.offset.y);
    new_line.lineToX(ctx, this.offset.x);

    this.line.moveTo(ctx);
    new_line = this.line.lineToY(ctx, -this.offset.y);
    new_line.lineToX(ctx, this.offset.x);
    ctx.stroke();
  }

  draw(ctx) {
    if (this.seed_flag == true) {
      this.draw_seed(ctx);
    } else {
      this.draw_normal(ctx);
    }
  }

  getNewBranches(seed_flag) {
    const new_point1 = new Branch(
      new Line(new Point(this.line.x + this.offset.x, this.line.y + this.offset.y)),
      new Point(this.offset.x, this.offset.y / 2),
      seed_flag,
      this.id * 10 + 1
    );
    const new_point2 = new Branch(
      new Line(new Point(this.line.x + this.offset.x, this.line.y - this.offset.y)),
      new Point(this.offset.x, this.offset.y / 2),
      seed_flag,
      this.id * 10 + 2
    );
    return [new_point1, new_point2];
  }

  setUser(user1, user2) {
    this.user1 = user1;
    if (this.seed_flag == false) {
      console.log('add user2:' + user2);
      this.user2 = user2;
    }
  }

  drawSeedUser(ctx, position) {
    let tmp_offset = new Point(this.offset.x, 0);
    let line = this.line.copyOffset(tmp_offset);

    if (position == 'left') {
      tmp_offset = new Point(this.offset.x * 2, 5);
    } else {
      tmp_offset = new Point(20, 5);
    }
    const base_line = line.copyOffset(tmp_offset);

    ctx.font = '14px Arial';
    ctx.fillText(this.user1, base_line.x, base_line.y);
  }
  drawNotSeedUser(ctx, position) {
    let line1 = this.line.copyOffset(this.offset);
    const tmp_point = new Point(this.offset.x, -this.offset.y);
    let line2 = this.line.copyOffset(tmp_point);

    let tmp_offset;
    if (position == 'left') {
      tmp_offset = new Point(this.offset.x * 2, 5);
    } else {
      tmp_offset = new Point(20, 5);
    }
    const base_line1 = line1.copyOffset(tmp_offset);
    const base_line2 = line2.copyOffset(tmp_offset);

    ctx.font = '14px Arial';
    ctx.fillText(this.user1, base_line1.x, base_line1.y);
    ctx.fillText(this.user2, base_line2.x, base_line2.y);
  }

  drawUser(ctx, position) {
    if (this.seed_flag) {
      this.drawSeedUser(ctx, position);
    } else {
      this.drawNotSeedUser(ctx, position);
    }
  }

  print() {
    console.log(
      `user1=${this.user1}, user2=${this.user2}, (x,y)= (${this.line.x}, ${this.line.y})`
    );
  }
}
