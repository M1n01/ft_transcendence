import Line from './/Line.js';
import Point from './/Point.js';
import Branch from './/Branch.js';

const OffsetX = 400;
export default class TournmentChart {
  constructor(canvas, size) {
    this.canvas = canvas;
    this.size = size;
    this.leftBranches = [];
    this.rightBranches = [];
    this.offsetPoint;
    //this.participants = null;
  }

  setParticipants(participants) {
    if (this.size != participants.length) {
      return false;
    }

    //const seed_participants = this.leftBranches.filter((branch) => {})
    const leftEdge = this.leftBranches.filter((branch) => branch.edge_flag == true);
    const rightEdge = this.rightBranches.filter((branch) => branch.edge_flag == true);
    const edges = [...leftEdge, ...rightEdge];
    console.log('edges=' + edges);
    console.log('edges[0]=' + edges[0]);
    const seed_edges = edges.filter((edge) => edge.seed_flag == true);
    const not_seed_edges = edges.filter((edge) => edge.seed_flag == false);

    //for(let i=0;i<seed_edges.)
    seed_edges.forEach((edge, index) => {
      edge.setUser(participants[index]);
    });
    const offset = seed_edges.length;
    not_seed_edges.forEach((edge, index) => {
      const user1 = participants[offset + index];
      const user2 = participants[offset + index + 1];
      edge.setUser(user1, user2);
    });

    this.leftBranches.forEach((branch) => {
      branch.print();
    });

    return true;
  }

  setSeedFlag = (edges, seed_cnt) => {
    const seed_list = new Set();
    while (true) {
      if (seed_list.size >= seed_cnt) {
        break;
      }
      seed_list.add(parseInt(Math.random() * edges.length));
    }

    seed_list.forEach((i) => {
      edges[i].seed_flag = true;
    });
  };

  calcBranchDepth = (total) => {
    let cnt = 0;
    while (total > 1) {
      total = total / 2;
      cnt++;
    }
    return cnt - 1;
  };

  recurMakeBranch = (ctx, branch, cnt, maxCnt, branches) => {
    if (cnt >= maxCnt) {
      return;
    }
    //branch.write(ctx);
    const seed_flag = maxCnt - cnt == 1;
    let new_branches = branch.getNewBranches(seed_flag);
    branches.push(new_branches[0]);
    branches.push(new_branches[1]);
    this.recurMakeBranch(ctx, new_branches[0], cnt + 1, maxCnt, branches);
    this.recurMakeBranch(ctx, new_branches[1], cnt + 1, maxCnt, branches);
  };

  init = () => {
    const BranchDepth = this.calcBranchDepth(this.size);
    this.canvas.width = this.canvas.width + (BranchDepth - 1) * 100 + OffsetX;
    this.canvas.height = this.canvas.height + parseInt((BranchDepth * BranchDepth - 2) / 4) * 200;

    const ctx = this.canvas.getContext('2d');

    // 塗りつぶされた四角形
    //ctx.fillStyle = 'blue';

    // 線の色と太さ
    ctx.strokeStyle = 'black';
    ctx.lineWidth = 3;

    // キャンバスの幅と高さ
    const canvasWidth = this.canvas.width - OffsetX;
    const canvasHeight = this.canvas.height;

    // 円の中心座標（キャンバスの中央）
    const centerX = (canvasWidth + OffsetX) / 2;
    const centerY = canvasHeight / 2;
    const CanvasCenter = new Point(centerX, centerY);

    const LeftOffsetPoint = new Point(
      -(centerX - 250) / ((2 * parseInt(BranchDepth + 1)) / 2),
      (centerY - 10) / 2
    );
    const RightOffsetPoint = new Point(
      (centerX - 250) / ((2 * parseInt(BranchDepth + 1)) / 2),
      (centerY - 10) / 2
    );
    this.offsetPoint = RightOffsetPoint;

    const BaseWidthLength = RightOffsetPoint.x / 1.5;
    //const BaseHeightLength = RightOffsetPoint.y;

    const LeftOffBase = new Point(-BaseWidthLength, 0);
    const RightOffBase = new Point(BaseWidthLength, 0);

    let leftLine = new Line(CanvasCenter.copyOffset(LeftOffBase));
    let rightLine = new Line(CanvasCenter.copyOffset(RightOffBase));

    // center
    //line.print();

    // branch
    const leftBranch = new Branch(leftLine, LeftOffsetPoint, false, 1);
    const rightBranch = new Branch(rightLine, RightOffsetPoint, false, 2);

    //const JointBaseLeft = CanvasCenter.copyOffset(LeftOffsetPoint);
    //const JointBaseRight = CanvasCenter.copyOffset(RightOffsetPoint);
    this.leftBranches = [leftBranch];
    this.rightBranches = [rightBranch];

    this.recurMakeBranch(ctx, leftBranch, 1, BranchDepth, this.leftBranches);
    this.recurMakeBranch(ctx, rightBranch, 1, BranchDepth, this.rightBranches);

    //const branches_cnt = leftBranches.length + rightBranches.length;
    const leftEdge = this.leftBranches.filter((branch) => branch.edge_flag == true);
    const rightEdge = this.rightBranches.filter((branch) => branch.edge_flag == true);

    const seed_cnt = (leftEdge.length + rightEdge.length) * 2 - this.size;
    const seed_left_cnt = parseInt(seed_cnt / 2);
    const seed_right_cnt = seed_cnt - seed_left_cnt;

    this.setSeedFlag(leftEdge, seed_left_cnt);
    this.setSeedFlag(rightEdge, seed_right_cnt);
  };

  draw = () => {
    const ctx = this.canvas.getContext('2d');
    ctx.strokeStyle = 'blue';

    const left_branch = this.leftBranches[0];
    const right_branch = this.rightBranches[0];

    ctx.beginPath();
    const BaseWidthLength = this.offsetPoint.x / 1.5;

    left_branch.line.moveTo(ctx);
    left_branch.line.lineToX(ctx, BaseWidthLength);
    right_branch.line.moveTo(ctx);
    right_branch.line.lineToX(ctx, -BaseWidthLength);
    ctx.stroke();

    this.leftBranches.forEach((branch) => {
      branch.draw(ctx);
    });
    this.rightBranches.forEach((branch) => {
      branch.draw(ctx);
    });

    // キャンバスの幅と高さ
    //const canvasWidth = this.canvas.width;
    const canvasWidth = this.canvas.width - OffsetX;
    const canvasHeight = this.canvas.height;

    const centerX = (canvasWidth + OffsetX) / 2;
    const centerY = canvasHeight / 2;

    // 円の半径
    const radius = 5;
    // Center Red Circle
    ctx.fillStyle = 'red';
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
    ctx.fill();
  };
  drawParticipants = () => {
    const ctx = this.canvas.getContext('2d');
    const leftEdge = this.leftBranches.filter((branch) => branch.edge_flag == true);
    const rightEdge = this.rightBranches.filter((branch) => branch.edge_flag == true);

    leftEdge.forEach((edge) => {
      edge.drawUser(ctx, 'left');
    });
    rightEdge.forEach((edge) => {
      edge.drawUser(ctx, 'right');
    });
  };

  //});
}
