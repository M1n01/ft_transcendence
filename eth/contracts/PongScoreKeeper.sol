// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { Ownable } from '@openzeppelin/contracts/access/Ownable.sol';

contract PongScoreKeeper is Ownable {
  struct Match {
    uint256 matchId;
    uint256 createdAt;
    uint256 updatedAt;
    uint256 winner;
    int16 winnerScore;
    uint256 loser;
    int16 loserScore;
    bool isActive; // 試合の削除フラグ
  }

  mapping(uint256 => Match) public matches;
  uint256 public nextMatchId;

  constructor(address initialOwner) Ownable(initialOwner) {}

  event MatchCreated(uint256 matchId, uint256 createdAt);
  event MatchUpdated(uint256 matchId, uint256 updatedAt);
  event MatchStatusChanged(uint256 matchId, bool isActive);

  // POST method
  function createMatch(
    uint256 _winner,
    int16 _winnerScore,
    uint256 _loser,
    int16 _loserScore
  ) external onlyOwner {
    require(_winner != _loser, 'Winner and loser cannot be the same');
    require(matches[nextMatchId].createdAt == 0, 'Match ID already exists'); // Solidityでは存在しないキーにアクセスした場合、型のデフォ値が返されるためセグフォしない

    matches[nextMatchId] = Match(
      nextMatchId,
      block.timestamp,
      0,
      _winner,
      _winnerScore,
      _loser,
      _loserScore,
      true
    );

    emit MatchCreated(nextMatchId, block.timestamp);

    nextMatchId++;
  }

  // GET method
  function getMatch(uint256 _matchId) external view onlyOwner returns (Match memory) {
    require(matches[_matchId].createdAt != 0, 'Match not found');
    return matches[_matchId];
  }

  // GET method
  function getAllMatches(bool _onlyActive) external view returns (Match[] memory) {
    uint256 count = 0;
    for (uint256 i = 0; i < nextMatchId; i++) {
      if (matches[i].createdAt != 0 && (matches[i].isActive || !_onlyActive)) {
        count++;
      }
    }

    Match[] memory _matches = new Match[](count);
    uint256 index = 0;
    for (uint256 i = 0; i < nextMatchId; i++) {
      if (matches[i].createdAt != 0 && (matches[i].isActive || !_onlyActive)) {
        _matches[index] = matches[i];
        index++;
      }
    }
    return _matches;
  }

  // GET method
  function getMatchesByUserId(
    uint256 _userId,
    bool _onlyActive
  ) external view returns (Match[] memory) {
    uint256 count = 0;
    // 関連するゲームの数を数える
    for (uint256 i = 0; i < nextMatchId; i++) {
      if (
        matches[i].winner == _userId ||
        (matches[i].loser == _userId && (matches[i].isActive || !_onlyActive))
      ) {
        count++;
      }
    }

    require(count > 0, 'No matches found for the given user ID');

    Match[] memory _matches = new Match[](count);
    uint256 index = 0;
    // 関連するゲームを配列に追加
    for (uint256 i = 0; i < nextMatchId; i++) {
      if (
        (matches[i].winner == _userId || matches[i].loser == _userId) &&
        (matches[i].isActive || !_onlyActive)
      ) {
        _matches[index] = matches[i];
        index++;
      }
    }
    return _matches;
  }

  // PUT method
  function updateMatch(
    uint256 _matchId,
    uint256 _winner,
    int16 _winnerScore,
    uint256 _loser,
    int16 _loserScore
  ) external onlyOwner {
    require(matches[_matchId].createdAt != 0, 'Match not found');
    require(_winner != _loser, 'Winner and loser cannot be the same');

    Match storage matchData = matches[_matchId];
    matchData.winner = _winner;
    matchData.winnerScore = _winnerScore;
    matchData.loser = _loser;
    matchData.loserScore = _loserScore;
    matchData.updatedAt = block.timestamp;

    emit MatchUpdated(_matchId, block.timestamp);
  }

  // DELETE method
  function toggleMatchStatus(uint256 _matchId) external onlyOwner {
    require(matches[_matchId].createdAt != 0, 'Match not found');

    Match storage matchData = matches[_matchId];
    matchData.isActive = !matchData.isActive;
    matchData.updatedAt = block.timestamp;

    emit MatchStatusChanged(_matchId, matchData.isActive);
  }
}
