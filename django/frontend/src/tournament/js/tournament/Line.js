import Point from './Point.js';
export default class Line extends Point {
  constructor(point) {
    console.log();
    super(point.x, point.y);
  }

  copy(point) {
    return new Line(point.x, point.y);
  }
  point() {
    return this.super;
  }
  moveTo(ctx) {
    ctx.moveTo(this.x, this.y);
  }
  lineToX(ctx, offsetX) {
    ctx.lineTo(this.x + offsetX, this.y);
    return new Line(new Point(this.x + offsetX, this.y));
  }
  lineToY(ctx, offsetY) {
    ctx.lineTo(this.x, this.y + offsetY);
    return new Line(new Point(this.x, this.y + offsetY));
  }
  lineToXY(ctx, offset) {
    ctx.lineTo(this.x + offset.x, this.y + offset.y);
    return new Line(new Point(this.x + offset.x, this.y + offset.y));
  }

  copyOffset(point) {
    const dx = this.x + point.x;
    const dy = this.y + point.y;
    const new_point = new Point(dx, dy);
    return new Line(new_point);
  }

  print() {
    //console.log(`x=${this.point.x}, y=${this.point.y}`);
    console.log(`(x, y)=(${this.x}, ${this.y})`);
  }
}
