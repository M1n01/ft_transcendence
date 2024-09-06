export default class Point {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }
  copy() {
    return new Point(this.x, this.y);
  }

  copyOffset(point) {
    const dx = this.x + point.x;
    const dy = this.y + point.y;
    const new_point = new Point(dx, dy);
    return new_point;
  }

  print() {
    console.log('`(${this.x}, ${this.y})`');
  }
}
