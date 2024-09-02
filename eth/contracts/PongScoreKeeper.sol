// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { Ownable } from '@openzeppelin/contracts/access/Ownable.sol';

contract PongScoreKeeper is Ownable {
  struct Match {
    uint256 matchId;
    uint256 createdAt;
    uint256 winner;
    int16 winnerScore;
    uint256 loser;
    int16 loserScore;
  }

  mapping(uint256 => Match) public matches;
  mapping(uint256 => bool) public matchExists;
  uint256 public nextMatchId;

  constructor(address initialOwner) Ownable(initialOwner) {}

  event MatchCreated(uint256 matchId, uint256 createdAt);

  function createMatch(
    uint256 _winner,
    int16 _winnerScore,
    uint256 _loser,
    int16 _loserScore
  ) external onlyOwner {
    require(_winner != _loser, 'Winner and loser cannot be the same');
    require(!matchExists[nextMatchId], 'Match ID already exists');

    matches[nextMatchId] = Match(
      nextMatchId,
      block.timestamp,
      _winner,
      _winnerScore,
      _loser,
      _loserScore
    );
    matchExists[nextMatchId] = true;

    emit MatchCreated(nextMatchId, block.timestamp);

    nextMatchId++;
  }

  function getMatch(uint256 _matchId) external view onlyOwner returns (Match memory) {
    require(matchExists[_matchId], 'Match not found');
    return matches[_matchId];
  }

  function getAllMatches() external view returns (Match[] memory) {
    uint256 count = 0;
    for (uint256 i = 0; i < nextMatchId; i++) {
      if (matchExists[i]) {
        count++;
      }
    }

    Match[] memory _matches = new Match[](count);
    uint256 index = 0;
    for (uint256 i = 0; i < nextMatchId; i++) {
      if (matchExists[i]) {
        _matches[index] = matches[i];
        index++;
      }
    }
    return _matches;
  }

  function getMatchCount() external view returns (uint256) {
    return nextMatchId;
  }

  function getMatchesByUserId(uint256 _userId) external view returns (Match[] memory) {
    uint256 count = 0;
    // 関連するゲームの数を数える
    for (uint256 i = 0; i < nextMatchId; i++) {
      if (matches[i].winner == _userId || matches[i].loser == _userId) {
        count++;
      }
    }

    require(count > 0, 'No matches found for the given user ID');

    Match[] memory _matches = new Match[](count);
    uint256 index = 0;
    // 関連するゲームを配列に追加
    for (uint256 i = 0; i < nextMatchId; i++) {
      if (matches[i].winner == _userId || matches[i].loser == _userId) {
        _matches[index] = matches[i];
        index++;
      }
    }
    return _matches;
  }
}
