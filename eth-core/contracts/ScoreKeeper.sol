// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { Ownable } from '@openzeppelin/contracts/access/Ownable.sol';

contract ScoreKeeper is Ownable {
  struct Game {
    uint256 matchId;
    uint256 winner;
    uint256 loser;
    int16 winnerScore;
    int16 loserScore;
  }

  Game[] public games;
  uint256 public nextGameId;

  constructor(address initialOwner) Ownable(initialOwner) {}

  function createGame(
    uint256 _winner,
    uint256 _loser,
    int16 _winnerScore,
    int16 _loserScore
  ) external onlyOwner {
    require(_winner != _loser, 'Winner and loser cannot be the same');
    // idが重複していないか確認
    for (uint256 i = 0; i < games.length; i++) {
      require(games[i].matchId != nextGameId, 'Match ID already exists');
    }

    games.push(Game(nextGameId, _winner, _loser, _winnerScore, _loserScore));
    nextGameId++;
  }

  function getGame(uint256 _matchId) external view returns (Game memory) {
    require(games[_matchId].matchId != 0, 'Match not found');
    return games[_matchId];
  }

  function getGameCount() external view returns (uint256) {
    return nextGameId;
  }
}
