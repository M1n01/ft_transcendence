import Point from './/Point.js';
//import Branch from './/Branch.js';
import Game from './/Game.js';

const OffsetX = 200;
export default class TournmentChart {
  constructor(parent, size) {
    this.parent = parent;
    this.size = size;
    this.leftBranches = [];
    this.rightBranches = [];
    this.offsetPoint;
    this.final = null;
  }

  recursiveSetGame(games, cur_game) {
    // 再帰終了条件
    if (cur_game.edge_flag == true) {
      const cur_game_data = games.find((game) => game.id == cur_game.id);

      let tmp_user1;
      let tmp_user2;

      if (cur_game_data.loser === '') {
        cur_game.seed_flag = true;
        cur_game.winner = cur_game_data.winner;
        cur_game.user1 = cur_game_data.winner;
        return;
      }

      if (cur_game_data.winner < cur_game_data.loser) {
        tmp_user1 = cur_game_data.winner;
        tmp_user2 = cur_game_data.loser;
      } else {
        tmp_user2 = cur_game_data.winner;
        tmp_user1 = cur_game_data.loser;
      }

      //console.log('cur_game winner=' + cur_game.winner);
      console.log('cur_game_data tmp_user1=' + tmp_user1);
      console.log('cur_game_data tmp_user2=' + tmp_user2);
      cur_game.user1 = tmp_user1;
      cur_game.user2 = tmp_user2;
      // 初期位置は、ユーザー名が大きい方が上になる
      /*
      if (tmp_user1 > tmp_user2) {
        console.log('user1:' + tmp_user1);
        console.log('user2:' + tmp_user2);
        cur_game.user1 = tmp_user1;
        cur_game.user2 = tmp_user2;
      } else {
        cur_game.user1 = tmp_user2;
        cur_game.user2 = tmp_user1;
      }
      */

      if (cur_game.user1 == cur_game_data.winner) {
        cur_game.winner = cur_game.user1;
      } else {
        cur_game.winner = cur_game.user2;
      }
      console.log('cur_game winner=' + cur_game.winner);
      console.log('cur_game_data winner=' + cur_game_data.winner);
      console.log('cur_game_data loser=' + cur_game_data.loser);
      //if (cur_game_data.loser == '') {
      //cur_game.seed_flag = true;
      //} else {
      //cur_game.user2 = tmp_user2;
      //cur_game.seed_flag = false;
      //}
      console.log('tmp_user1=' + tmp_user1);
      console.log('tmp_user2=' + tmp_user2);

      return;
    }
    console.log('set final No.5 cur_game=' + cur_game);

    const current_id = cur_game.id;
    const next_id1 = current_id * 10 + 1;
    const next_id2 = current_id * 10 + 2;

    const cur_game_data = games.find((game) => game.id == current_id);
    const next_game_data1 = games.find((game) => game.id == next_id1);
    const next_game_data2 = games.find((game) => game.id == next_id2);

    cur_game.user1 = next_game_data1.winner;
    cur_game.user2 = next_game_data2.winner;

    if (cur_game_data.winner == next_game_data1.winner) {
      cur_game.winner = next_game_data1.winner;
    } else {
      cur_game.winner = next_game_data2.winner;
    }
    console.log('cur_game.winner:' + cur_game.winner);
    console.log('cur_game.user1:' + cur_game.user1);
    console.log('cur_game.user2:' + cur_game.user2);

    let next_game1;
    let next_game2;
    if (String(next_game_data1.id)[0] == '1') {
      next_game1 = this.leftBranches.find((game) => game.id == next_game_data1.id);
    } else {
      next_game1 = this.rightBranches.find((game) => game.id == next_game_data1.id);
    }
    if (String(next_game_data2.id)[0] == '1') {
      next_game2 = this.leftBranches.find((game) => game.id == next_game_data2.id);
    } else {
      next_game2 = this.rightBranches.find((game) => game.id == next_game_data2.id);
    }

    this.recursiveSetGame(games, next_game1);
    this.recursiveSetGame(games, next_game2);
  }

  setGames(games) {
    console.log('set final No.3 cur_game=' + this.final);
    this.recursiveSetGame(games, this.final);
    //if (this.size != participants.length) {
    //return false;
    //}

    /*
    const current_id = game.id;
    const next_id1 = current_id * 10 + 1;
    const next_id2 = current_id * 10 + 2;

    const final = games.find((game) => game.id == '0');
    const semi_final1 = games.find((game) => game.id == '1');
    const semi_final2 = games.find((game) => game.id == '2');

    //this.final = new Game();

    this.final.user1 = semi_final1.winner;
    this.final.user2 = semi_final2.winner;
    if (final.winner == semi_final1.winner) {
      this.final.winner = semi_final1.winner;
    } else {
      this.final.winner = semi_final2.winner;
    }
    */
  }

  setParticipants(participants) {
    if (this.size != participants.length) {
      return false;
    }

    const leftEdge = this.leftBranches.filter((branch) => branch.edge_flag == true);
    const rightEdge = this.rightBranches.filter((branch) => branch.edge_flag == true);

    const seed_cnt = (leftEdge.length + rightEdge.length) * 2 - this.size;
    const seed_left_cnt = parseInt(seed_cnt / 2);
    const seed_right_cnt = seed_cnt - seed_left_cnt;

    this.setSeedFlag(leftEdge, seed_left_cnt);
    this.setSeedFlag(rightEdge, seed_right_cnt);

    //const seed_participants = this.leftBranches.filter((branch) => {})
    //const leftEdge = this.leftBranches.filter((branch) => branch.edge_flag == true);
    //const rightEdge = this.rightBranches.filter((branch) => branch.edge_flag == true);
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
      const tmp_user1 = participants[offset + index];
      const tmp_user2 = participants[offset + index + 1];
      if (tmp_user1 < tmp_user2) {
        edge.setUser(tmp_user1, tmp_user2);
      } else {
        edge.setUser(tmp_user2, tmp_user1);
      }
    });

    // this.leftBranches.forEach((branch) => {
    //   branch.print();
    // });

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
      edges[i].setSeed(true);
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

  recursiveMakeBranch = (ctx, branch, cnt, maxCnt, branches) => {
    if (cnt >= maxCnt) {
      console.log('end');
      return;
    }
    //branch.write(ctx);
    const edge_flag = maxCnt - cnt == 1;
    let new_branches = branch.getNewGames(edge_flag);
    branches.push(new_branches[0]);
    branches.push(new_branches[1]);
    this.recursiveMakeBranch(ctx, new_branches[0], cnt + 1, maxCnt, branches);
    this.recursiveMakeBranch(ctx, new_branches[1], cnt + 1, maxCnt, branches);
  };

  init = () => {
    const BranchDepth = this.calcBranchDepth(this.size);
    const initWidth = this.parent.clientWidth;
    const initHeight = this.parent.clientHeight;
    const curWidth = initWidth + (BranchDepth - 1) * 50 + OffsetX;
    const curHeight = initHeight + parseInt((BranchDepth * BranchDepth - 4) / 4) * 150;
    this.parent.style.width = `${curWidth}px`;
    this.parent.style.height = `${curHeight}px`;

    const ctx = document.createElement('div');

    // 塗りつぶされた四角形
    //ctx.fillStyle = 'blue';

    // 線の色と太さ
    //ctx.strokeStyle = 'black';
    //ctx.lineWidth = 3;

    // キャンバスの幅と高さ
    const canvasWidth = this.parent.clientWidth - OffsetX;
    const canvasHeight = this.parent.clientHeight;

    // 円の中心座標（キャンバスの中央）
    const centerX = (canvasWidth + OffsetX) / 2;
    const centerY = canvasHeight / 2;

    const CanvasCenter = new Point(centerX, centerY);
    const LeftOffsetPoint = new Point(
      parseInt(-(centerX - 150) / ((2 * parseInt(BranchDepth + 1)) / 2)),
      parseInt((centerY - 10) / 2)
    );
    const RightOffsetPoint = new Point(
      parseInt((centerX - 150) / ((2 * parseInt(BranchDepth + 1)) / 2)),
      parseInt((centerY - 10) / 2)
    );

    this.offsetPoint = RightOffsetPoint;

    const BaseWidthLength = parseInt(RightOffsetPoint.x);
    //const BaseHeightLength = RightOffsetPoint.y;

    const offset = new Point(-BaseWidthLength, 0);
    const LeftOffBase = new Point(-BaseWidthLength, 0);
    const RightOffBase = new Point(BaseWidthLength, 0);

    let leftPoint = CanvasCenter.copyOffset(LeftOffBase);
    let rightPoint = CanvasCenter.copyOffset(RightOffBase);

    console.log('set final No.1');
    this.final = new Game(CanvasCenter, offset, false, 0, '', CanvasCenter);
    console.log('set final No.2 final=' + this.final);
    const leftBranch = new Game(leftPoint, LeftOffsetPoint, false, 1, 'left', this.final);
    const rightBranch = new Game(rightPoint, RightOffsetPoint, false, 2, 'right', this.final);
    console.log('init No.5');

    //const JointBaseLeft = CanvasCenter.copyOffset(LeftOffsetPoint);
    //const JointBaseRight = CanvasCenter.copyOffset(RightOffsetPoint);
    this.leftBranches = [leftBranch];
    this.rightBranches = [rightBranch];

    console.log('init No.6');
    this.recursiveMakeBranch(ctx, leftBranch, 1, BranchDepth, this.leftBranches);
    console.log('init No.7');
    this.recursiveMakeBranch(ctx, rightBranch, 1, BranchDepth, this.rightBranches);
    console.log('init No.8');

    //const branches_cnt = leftBranches.length + rightBranches.length;
    /*
    const leftEdge = this.leftBranches.filter((branch) => branch.edge_flag == true);
    const rightEdge = this.rightBranches.filter((branch) => branch.edge_flag == true);

    const seed_cnt = (leftEdge.length + rightEdge.length) * 2 - this.size;
    const seed_left_cnt = parseInt(seed_cnt / 2);
    const seed_right_cnt = seed_cnt - seed_left_cnt;

    this.setSeedFlag(leftEdge, seed_left_cnt);
    this.setSeedFlag(rightEdge, seed_right_cnt);
    */

    return;
  };

  draw = () => {
    //const ctx = this.canvas.getContext('2d');
    //ctx.strokeStyle = 'blue';

    //const left_branch = this.leftBranches[0];
    //const right_branch = this.rightBranches[0];

    //ctx.beginPath();
    //const BaseWidthLength = this.offsetPoint.x / 1.5;

    /*
    left_branch.line.moveTo(ctx);
    left_branch.line.lineToX(ctx, BaseWidthLength);
    right_branch.line.moveTo(ctx);
    right_branch.line.lineToX(ctx, -BaseWidthLength);
    */
    //ctx.stroke();

    this.final.draw(this.parent, null);
    this.leftBranches.forEach((game) => {
      const next_id = parseInt(game.id / 10);
      const next_game = this.leftBranches.find((game) => game.id == next_id);
      game.draw(this.parent, next_game);
    });
    this.rightBranches.forEach((game) => {
      const next_id = parseInt(game.id / 10);
      const next_game = this.rightBranches.find((game) => game.id == next_id);
      game.draw(this.parent, next_game);
    });

    // キャンバスの幅と高さ
    //const canvasWidth = this.canvas.width;
    //const canvasWidth = this.canvas.width - OffsetX;
    //const canvasHeight = this.canvas.height;
    //const initWidth = this.parent.clientWidth;
    //const initHeight = this.parent.clientHeight;

    //const centerX = (initWidth + OffsetX) / 2;
    //const centerY = initHeight / 2;

    // 円の半径
    //const radius = 5;
    // Center Red Circle
    //ctx.fillStyle = 'red';
    //ctx.beginPath();
    ////ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
    //ctx.fill();
  };
  drawParticipants = () => {
    //const ctx = this.canvas.getContext('2d');
    const leftEdge = this.leftBranches.filter((branch) => branch.edge_flag == true);
    const rightEdge = this.rightBranches.filter((branch) => branch.edge_flag == true);

    leftEdge.forEach((edge) => {
      edge.drawUser(this.parent);
    });
    rightEdge.forEach((edge) => {
      edge.drawUser(this.parent);
    });
  };

  //});
}
