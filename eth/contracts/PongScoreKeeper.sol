// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { Ownable } from '@openzeppelin/contracts/access/Ownable.sol';
import { Pausable } from '@openzeppelin/contracts/utils/Pausable.sol';

contract PongScoreKeeper is Ownable, Pausable {
  struct Match {
    uint256 matchId;
    uint256 createdAt;
    uint256 player1;
    uint16 player1Score;
    uint256 player2;
    uint16 player2Score;
    bool isActive; // Matchの削除フラグ
  }

  mapping(uint256 => Match) public matches;
  uint256 public nextMatchId;

  event MatchCreated(
    uint256 indexed matchId,
    uint256 createdAt,
    uint256 indexed player1,
    uint256 indexed player2
  );
  event MatchStatusChanged(uint256 indexed matchId, bool isActive);

  constructor(address initialOwner) Ownable(initialOwner) {}

  // POST method
  function createMatch(
    uint256 _player1,
    uint16 _player1Score,
    uint256 _player2,
    uint16 _player2Score
  ) external onlyOwner whenNotPaused {
    require(_player1 != _player2, 'Winner and player2 cannot be the same');
    require(_player1Score > _player2Score, 'Winner score must be higher');

    uint256 matchId = nextMatchId;
    matches[matchId] = Match(
      matchId,
      block.timestamp,
      _player1,
      _player1Score,
      _player2,
      _player2Score,
      true
    );
    nextMatchId++;
    emit MatchCreated(matchId, block.timestamp, _player1, _player2);
  }

  function getMatch(uint256 _matchId) external view returns (Match memory) {
    require(matches[_matchId].createdAt != 0, 'Match not found');
    return matches[_matchId];
  }

  // GET method
  function getAllMatches(
    bool _onlyActive,
    uint256 _page,
    uint256 _limit
  ) external view returns (Match[] memory, uint256) {
    require(_limit > 0 && _limit <= 100, 'Invalid limit');
    uint256 start = _page * _limit;
    uint256 end = start + _limit;
    if (end > nextMatchId) {
      end = nextMatchId;
    }

    Match[] memory _matches = new Match[](end - start);

    uint256 index = 0;
    for (uint256 i = start; i < end; i++) {
      if (matches[i].createdAt != 0 && (matches[i].isActive || !_onlyActive)) {
        _matches[index] = matches[i];
        index++;
      }
    }

    // Resize the array to remove empty slots
    assembly {
      mstore(_matches, index)
    }

    return (_matches, nextMatchId);
  }

  function getMatchesByUserId(
    uint256 _userId,
    bool _onlyActive,
    uint256 _page,
    uint256 _limit
  ) external view returns (Match[] memory, uint256) {
    require(_limit > 0 && _limit <= 100, 'Invalid limit');
    uint256 start = _page * _limit;

    Match[] memory _matches = new Match[](_limit);
    uint256 index = 0;
    uint256 totalMatches = 0;

    for (uint256 i = 0; i < nextMatchId && index < _limit; i++) {
      if (
        (matches[i].player1 == _userId || matches[i].player2 == _userId) &&
        (matches[i].isActive || !_onlyActive)
      ) {
        if (totalMatches >= start) {
          _matches[index] = matches[i];
          index++;
        }
        totalMatches++;
      }
    }

    // Resize the array to remove empty slots
    assembly {
      mstore(_matches, index)
    }

    return (_matches, totalMatches);
  }

  // DELETE method
  function toggleMatchStatus(uint256 _matchId) external onlyOwner whenNotPaused {
    require(matches[_matchId].createdAt != 0, 'Match not found');

    Match storage matchData = matches[_matchId];
    matchData.isActive = !matchData.isActive;

    emit MatchStatusChanged(_matchId, matchData.isActive);
  }

  function pause() external onlyOwner {
    _pause();
  }

  function unpause() external onlyOwner {
    _unpause();
  }
}
