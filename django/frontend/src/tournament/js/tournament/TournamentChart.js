import Point from './Point.js';
//import Branch from './/Branch.js';
import Game from './Game.js';

const OffsetX = 200;
export default class TournamentChart {
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
    if (cur_game == null) {
      return;
    }
    // 再帰終了条件
    if (cur_game.edge_flag == true) {
      const cur_game_data = games.find((game) => game.id == cur_game.id);

      if (cur_game_data.player2 === '') {
        cur_game.seed_flag = true;
        cur_game.is_end = true;
        cur_game.winner = cur_game_data.player1;
        cur_game.user1 = cur_game_data.player1;
        return;
      }

      /*
      if (cur_game_data.winner < cur_game_data.loser) {
        tmp_user1 = cur_game_data.winner;
        tmp_user2 = cur_game_data.loser;
      } else {
        tmp_user2 = cur_game_data.winner;
        tmp_user1 = cur_game_data.loser;
      }
      */

      cur_game.user1 = cur_game_data.player1;
      cur_game.user2 = cur_game_data.player2;

      if (
        cur_game_data.player1_score > cur_game_data.player2_score &&
        cur_game_data.player1_score >= 5
      ) {
        cur_game.winner = cur_game.user1;
      } else if (
        cur_game_data.player1_score < cur_game_data.player2_score &&
        cur_game_data.player2_score >= 5
      ) {
        cur_game.winner = cur_game.user2;
      } else {
        cur_game.winner = '';
      }
      return;
    }

    const cur_game_data = games.find((game) => game.id == cur_game.id);
    if (cur_game_data) {
      if (
        cur_game_data.player1_score > cur_game_data.player2_score &&
        cur_game_data.player1_score >= 5
      ) {
        cur_game.winner = cur_game_data.player1;
        cur_game.user1 = cur_game_data.player1;
        cur_game.user2 = cur_game_data.player2;
      } else if (
        cur_game_data.player1_score < cur_game_data.player2_score &&
        cur_game_data.player2_score >= 5
      ) {
        cur_game.winner = cur_game_data.player2;
        cur_game.user1 = cur_game_data.player1;
        cur_game.user2 = cur_game_data.player2;
      } else {
        cur_game.winner = '';
      }
    }

    const current_id = cur_game.id;
    const next_id1 = current_id * 10 + 1;
    const next_id2 = current_id * 10 + 2;

    //const cur_game_data = games.find((game) => game.id == current_id);
    const next_game_data1 = games.find((game) => game.id == next_id1);
    const next_game_data2 = games.find((game) => game.id == next_id2);

    if (next_game_data1 && next_game_data1.is_end) {
      if (next_game_data1.player1_score > next_game_data1.player2_score) {
        cur_game.user1 = next_game_data1.player1;
      } else if (next_game_data1.player1_score < next_game_data1.player2_score) {
        cur_game.user1 = next_game_data1.player2;
      } else {
        cur_game.user1 = '';
      }
    }
    //cur_game.user1 = next_game_data1.winner;
    //cur_game.user2 = next_game_data2.winner;

    if (next_game_data2 && next_game_data2.is_end) {
      if (next_game_data2.player1_score > next_game_data2.player2_score) {
        cur_game.user2 = next_game_data2.player1;
      } else if (next_game_data1.player1_score < next_game_data2.player2_score) {
        cur_game.user2 = next_game_data2.player2;
      } else {
        cur_game.user2 = '';
      }
    }

    /*
    if (cur_game.player1_score > cur_game.player2_score && cur_game.player1_score >= 5) {
      cur_game.winner = cur_game.user1;
    } else if (cur_game.player1_score < cur_game.player2_score && cur_game.player2_score >= 5) {
      cur_game.winner = cur_game.user2;
    } else {
      cur_game.winner = '';
    }
    */

    let next_game1;
    let next_game2;
    if (next_game_data1 && String(next_game_data1.id)[0] == '1') {
      next_game1 = this.leftBranches.find((game) => game.id == next_game_data1.id);
    } else if (next_game_data1) {
      next_game1 = this.rightBranches.find((game) => game.id == next_game_data1.id);
    }
    if (next_game_data2 && String(next_game_data2.id)[0] == '1') {
      next_game2 = this.leftBranches.find((game) => game.id == next_game_data2.id);
    } else if (next_game_data2) {
      next_game2 = this.rightBranches.find((game) => game.id == next_game_data2.id);
    }

    this.recursiveSetGame(games, next_game1);
    this.recursiveSetGame(games, next_game2);
  }

  setGames(games) {
    this.recursiveSetGame(games, this.final);
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

    cnt = 0;
    total = total - 1;
    while (total >= 1) {
      total = parseInt(total / 2);
      cnt++;
    }
    return cnt - 1;
  };

  recursiveMakeBranch = (ctx, branch, cnt, maxCnt, branches) => {
    if (cnt >= maxCnt) {
      return;
    }
    const edge_flag = maxCnt - cnt == 1;
    let new_branches = branch.getNewGames(edge_flag);
    branches.push(new_branches[0]);
    branches.push(new_branches[1]);
    this.recursiveMakeBranch(ctx, new_branches[0], cnt + 1, maxCnt, branches);
    this.recursiveMakeBranch(ctx, new_branches[1], cnt + 1, maxCnt, branches);
  };

  init = () => {
    const BranchDepth = this.calcBranchDepth(this.size);
    //const initWidth = this.parent.clientWidth;
    //const initHeight = this.parent.clientHeight;
    const initWidth = 400;
    const initHeight = 200;
    const curWidth = initWidth + (BranchDepth - 1) * 50 + OffsetX;
    const curHeight = initHeight + parseInt((BranchDepth * BranchDepth - 4) / 4) * 150;
    this.parent.style.width = `${curWidth}px`;
    this.parent.style.height = `${curHeight}px`;

    const ctx = document.createElement('div');

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
    const offset = new Point(-BaseWidthLength, 0);
    const LeftOffBase = new Point(-BaseWidthLength, 0);
    const RightOffBase = new Point(BaseWidthLength, 0);

    let leftPoint = CanvasCenter.copyOffset(LeftOffBase);
    let rightPoint = CanvasCenter.copyOffset(RightOffBase);

    this.final = new Game(CanvasCenter, offset, false, 0, '', CanvasCenter);

    const leftBranch = new Game(leftPoint, LeftOffsetPoint, false, 1, 'left', this.final);
    const rightBranch = new Game(rightPoint, RightOffsetPoint, false, 2, 'right', this.final);

    let cnt = 1;
    if (this.size == 4) {
      leftBranch.edge_flag = true;
      rightBranch.edge_flag = true;
      cnt = 1;
    }

    this.leftBranches = [leftBranch];
    this.rightBranches = [rightBranch];

    this.recursiveMakeBranch(ctx, leftBranch, cnt, BranchDepth, this.leftBranches);
    this.recursiveMakeBranch(ctx, rightBranch, cnt, BranchDepth, this.rightBranches);

    return;
  };

  draw = () => {
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
  };
  drawParticipants = () => {
    const leftEdge = this.leftBranches.filter((branch) => branch.edge_flag == true);
    const rightEdge = this.rightBranches.filter((branch) => branch.edge_flag == true);

    const height_offset_flag = leftEdge.length == 1 && rightEdge.length;
    leftEdge.forEach((edge) => {
      edge.drawUser(this.parent, height_offset_flag);
    });
    rightEdge.forEach((edge) => {
      edge.drawUser(this.parent, height_offset_flag);
    });
  };
}
