// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract PongScoreKeeper {
  struct Match {
    uint256 matchId;
    bytes16 tournamentId;
    bytes16 player1;
    bytes16 player2;
    uint256 createdAt;
    uint16 player1Score;
    uint16 player2Score;
    uint16 round;
    bool isActive; // Matchの削除フラグ
  }

  mapping(uint256 => Match) public matches;
  uint256 public nextMatchId;

  address public immutable owner;

  event MatchCreated(
    uint256 indexed matchId,
    bytes16 tournamentId,
    uint256 createdAt,
    bytes16 indexed player1,
    bytes16 indexed player2,
    uint16 round
  );

  event MatchStatusChanged(uint256 indexed matchId, bool isActive);

  modifier onlyOwner() {
    require(msg.sender == owner, 'Not owner');
    _;
  }

  constructor() {
    owner = msg.sender;
  }

  // POST method
  function createMatch(
    bytes16 _tournamentId,
    bytes16 _player1,
    uint16 _player1Score,
    bytes16 _player2,
    uint16 _player2Score,
    uint16 _round
  ) external onlyOwner {
    require(_player1 != _player2, 'player1 and player2 cannot be the same');

    matches[nextMatchId] = Match(
      nextMatchId,
      _tournamentId,
      _player1,
      _player2,
      block.timestamp,
      _player1Score,
      _player2Score,
      _round,
      true // アクティブフラグ
    );
    emit MatchCreated(nextMatchId, _tournamentId, block.timestamp, _player1, _player2, _round);
    nextMatchId++;
  }

  function getMatch(uint256 _matchId, bool _onlyActive) external view returns (Match memory) {
    require(matches[_matchId].createdAt != 0, 'Match not found');
    Match memory _match = matches[_matchId];
    if (_onlyActive && !_match.isActive) {
      revert('Match not found');
    }
    return _match;
  }

  // GET method
  function getAllMatches(bool _onlyActive) external view returns (Match[] memory) {
    uint256 _totalMatches = nextMatchId;
    Match[] memory _allMatches = new Match[](_totalMatches);
    uint256 _count = 0;

    for (uint256 i = 0; i < _totalMatches; i++) {
      if (matches[i].createdAt != 0 && (!_onlyActive || matches[i].isActive)) {
        _allMatches[_count] = matches[i];
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
  function deleteMatch(uint256 _matchId) external onlyOwner {
    require(matches[_matchId].createdAt != 0, 'Match not found');

    Match storage matchData = matches[_matchId];
    matchData.isActive = !matchData.isActive;

    emit MatchStatusChanged(_matchId, matchData.isActive);
  }
}
