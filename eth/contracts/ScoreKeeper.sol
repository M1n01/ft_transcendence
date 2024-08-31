// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { Ownable } from '@openzeppelin/contracts/access/Ownable.sol';

contract ScoreKeeper is Ownable {
  struct Game {
    uint256 matchId;
    uint256 createdAt;
    uint256 winner;
    int16 winnerScore;
    uint256 loser;
    int16 loserScore;
  }

  mapping(uint256 => Game) public games;
  mapping(uint256 => bool) public gameExists;
  uint256 public nextGameId;

  constructor(address initialOwner) Ownable(initialOwner) {}

  function createGame(
    uint256 _winner,
    int16 _winnerScore,
    uint256 _loser,
    int16 _loserScore
  ) external onlyOwner {
    require(_winner != _loser, 'Winner and loser cannot be the same');
    require(!gameExists[nextGameId], 'Match ID already exists');

    games[nextGameId] = Game(
      nextGameId,
      block.timestamp,
      _winner,
      _winnerScore,
      _loser,
      _loserScore
    );
    gameExists[nextGameId] = true;
    nextGameId++;
  }

  function getGame(uint256 _matchId) external view onlyOwner returns (Game memory) {
    require(gameExists[_matchId], 'Match not found');
    return games[_matchId];
  }

  function getAllGame() external view returns (Game[] memory) {
    uint256 count = 0;
    for (uint256 i = 0; i < nextGameId; i++) {
      if (gameExists[i]) {
        count++;
      }
    }

    Game[] memory _games = new Game[](count);
    uint256 index = 0;
    for (uint256 i = 0; i < nextGameId; i++) {
      if (gameExists[i]) {
        _games[index] = games[i];
        index++;
      }
    }
    return _games;
  }

  function getGameCount() external view returns (uint256) {
    return nextGameId;
  }

  function findGameByUserId(uint256 _userId) external view returns (Game[] memory) {
    uint256 count = 0;
    // 関連するゲームの数を数える
    for (uint256 i = 0; i < nextGameId; i++) {
      if (games[i].winner == _userId || games[i].loser == _userId) {
        count++;
      }
    }

    require(count > 0, 'No games found for the given user ID');

    Game[] memory _games = new Game[](count);
    uint256 index = 0;
    // 関連するゲームを配列に追加
    for (uint256 i = 0; i < nextGameId; i++) {
      if (games[i].winner == _userId || games[i].loser == _userId) {
        _games[index] = games[i];
        index++;
      }
    }
    return _games;
  }
}
