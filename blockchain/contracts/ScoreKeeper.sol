// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { Ownable } from '@openzeppelin/contracts/access/Ownable.sol';

contract ScoreKeeper is Ownable {
  constructor(address initialOwner) Ownable(initialOwner) {}

  mapping(address => uint256) private scores;

  function setScore(address _user, uint256 _score) public onlyOwner {
    scores[_user] = _score;
  }

  function getScore(address _user) public view returns (uint256) {
    return scores[_user];
  }
}
