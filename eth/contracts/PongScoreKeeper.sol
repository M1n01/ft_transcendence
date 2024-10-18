// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract PongScoreKeeper {
  struct Match {
    uint256 createdAt;
    bytes16 tournamentId;
    bytes16 player1;
    bytes16 player2;
    uint16 player1Score;
    uint16 player2Score;
    uint16 round;
    bool isActive; // Matchの削除フラグ
  }

  mapping(bytes32 => Match) public matches;
  bytes32[] public matchHashes;

  event MatchCreated(
    bytes32 indexed matchHash,
    bytes16 tournamentId,
    uint256 createdAt,
    bytes16 indexed player1,
    bytes16 indexed player2,
    uint16 round
  );
  event MatchStatusChanged(bytes32 indexed matchHash, bool isActive);

  address public immutable owner;
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

    bytes32 _transactionHash = keccak256(
      abi.encodePacked(_tournamentId, _player1, _player1Score, _player2, _player2Score, _round)
    );

    Match memory _newMatch = Match({
      createdAt: block.timestamp,
      tournamentId: _tournamentId,
      player1: _player1,
      player2: _player2,
      player1Score: _player1Score,
      player2Score: _player2Score,
      round: _round,
      isActive: true
    });

    matches[_transactionHash] = _newMatch;
    matchHashes.push(_transactionHash);

    emit MatchCreated(_transactionHash, _tournamentId, block.timestamp, _player1, _player2, _round);
  }

  function getMatch(
    bytes32 _transactionHash,
    bool _onlyActive
  ) external view returns (Match memory) {
    require(matches[_transactionHash].createdAt != 0, 'Match not found');

    Match memory _match = matches[_transactionHash];
    if (_onlyActive && !_match.isActive) {
      revert('Match not found');
    }
    return _match;
  }

  // GET method
  function getAllMatches(bool _onlyActive) external view returns (Match[] memory) {
    Match[] memory _allMatches = new Match[](matchHashes.length);

    uint256 _count = 0;
    for (uint256 i = 0; i < matchHashes.length; i++) {
      if (
        matches[matchHashes[i]].createdAt != 0 && (!_onlyActive || matches[matchHashes[i]].isActive)
      ) {
        _allMatches[_count] = matches[matchHashes[i]];
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
  function deleteMatch(bytes32 _transactionHash) external onlyOwner {
    require(matches[_transactionHash].createdAt != 0, 'Match not found');

    Match storage matchData = matches[_transactionHash];
    matchData.isActive = !matchData.isActive;

    emit MatchStatusChanged(_transactionHash, matchData.isActive);
  }
}
