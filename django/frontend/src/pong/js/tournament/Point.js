export default class Point {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }
  copy(point) {
    return new Point(point.x, point.y);
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
