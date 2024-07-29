// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { Ownable } from '@openzeppelin/contracts/access/Ownable.sol';

contract ScoreKeeper is Ownable {
  struct Player {
    uint256 id;
    uint256 score;
  }

  struct Match {
    uint256 matchId;
    Player player;
    Player opponent;
  }

  mapping(uint256 => Match) public matches;
  uint256[] public matchIds;

  constructor(address initialOwner) Ownable(initialOwner) {}

  function addMatch(
    uint256 _matchId,
    uint256 _playerId,
    uint256 _playerScore,
    uint256 _opponentId,
    uint256 _opponentScore
  ) public onlyOwner {
    require(_matchId > 0, 'Match ID must be greater than 0');
    require(
      _matchId > matchIds.length,
      'Match ID must be greater than the current number of matches'
    );
    require(_playerId > 0, 'Player ID must be greater than 0');
    require(_opponentId > 0, 'Opponent ID must be greater than 0');
    Player memory player = Player(_playerId, _playerScore);
    Player memory opponent = Player(_opponentId, _opponentScore);
    matches[_matchId] = Match(_matchId, player, opponent);
    matchIds.push(_matchId);
  }

  function getMatch(uint256 _matchId) public view returns (Match memory) {
    require(matches[_matchId].matchId != 0, 'Match not found');
    return matches[_matchId];
  }

  function getMatchCount() public view returns (uint256) {
    return matchIds.length;
  }
}
