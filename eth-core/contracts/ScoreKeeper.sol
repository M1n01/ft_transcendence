// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { Ownable } from '@openzeppelin/contracts/access/Ownable.sol';

contract ScoreKeeper is Ownable {
  struct Game {
    uint256 matchId;
    address winner;
    address loser;
    int16 winnerScore;
    int16 loserScore;
  }

  Game[] public games;
  uint256 public nextGameId;

  constructor(address initialOwner) Ownable(initialOwner) {}

  function createGame(
    address _winner,
    address _loser,
    int16 _winnerScore,
    int16 _loserScore
  ) external onlyOwner {
    games.push(Game(nextGameId, _winner, _loser, _winnerScore, _loserScore));
    nextGameId++;
  }

  function createGame(uint256 _matchId) external view returns (Game memory) {
    require(games[_matchId].matchId != 0, 'Match not found');
    return games[_matchId];
  }

  function getGameCount() external view returns (uint256) {
    return nextGameId;
  }
}
