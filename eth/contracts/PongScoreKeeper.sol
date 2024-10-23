// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract PongScoreKeeper {
  struct Match {
    uint128 matchId;
    uint128 tournamentId;
    uint256 createdAt;
    uint128 player1;
    uint128 player2;
    uint16 player1Score;
    uint16 player2Score;
    uint16 round;
    bool isActive; // Matchの削除フラグ
  }

  mapping(uint128 => Match) public matches;
  uint128[] public matchIds;

  address public immutable owner;

  event MatchCreated(
    uint128 indexed matchId,
    uint128 tournamentId,
    uint256 createdAt,
    uint128 indexed player1,
    uint128 indexed player2,
    uint16 round
  );

  event MatchStatusChanged(uint128 indexed matchId, bool isActive);

  modifier onlyOwner() {
    require(msg.sender == owner, 'Not owner');
    _;
  }

  constructor() {
    owner = msg.sender;
  }

  // POST method
  function createMatch(
    uint128 _matchId,
    uint128 _tournamentId,
    uint128 _player1,
    uint128 _player2,
    uint16 _player1Score,
    uint16 _player2Score,
    uint16 _round
  ) external onlyOwner {
    require(_player1 != _player2, 'player1 and player2 cannot be the same');

    matches[_matchId] = Match(
      _matchId,
      _tournamentId,
      block.timestamp,
      _player1,
      _player2,
      _player1Score,
      _player2Score,
      _round,
      true // アクティブフラグ
    );
    matchIds.push(_matchId);
    emit MatchCreated(_matchId, _tournamentId, block.timestamp, _player1, _player2, _round);
  }

  function getMatch(uint128 _matchId, bool _onlyActive) external view returns (Match memory) {
    require(matches[_matchId].createdAt != 0, 'Match not found');
    Match memory _match = matches[_matchId];
    if (_onlyActive && !_match.isActive) {
      revert('Match not found');
    }
    return _match;
  }

  // GET method
  function getAllMatches(bool _onlyActive) external view returns (Match[] memory) {
    uint256 _totalMatches = matchIds.length;
    Match[] memory _allMatches = new Match[](_totalMatches);

    uint256 _count = 0;
    for (uint256 i = 0; i < _totalMatches; i++) {
      uint128 _matchId = matchIds[i];
      if (matches[_matchId].createdAt != 0 && (!_onlyActive || matches[_matchId].isActive)) {
        _allMatches[_count] = matches[_matchId];
        _count++;
      }
    }

    // Resize the array to remove empty slots
    assembly {
      mstore(_allMatches, _count)
    }
    return _allMatches;
  }

  // DELETE method
  function deleteMatch(uint128 _matchId) external onlyOwner {
    require(matches[_matchId].createdAt != 0, 'Match not found');

    Match storage matchData = matches[_matchId];
    matchData.isActive = !matchData.isActive;

    emit MatchStatusChanged(_matchId, matchData.isActive);
  }
}
