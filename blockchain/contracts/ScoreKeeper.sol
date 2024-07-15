// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/access/Ownable.sol";

contract ScoreKeeper is Ownable {
    constructor(address initialOwner) Ownable(initialOwner) {
    }

    mapping(address => uint256) private scores;

    function setScore(uint256 _score) public {
        scores[msg.sender] = _score;
    }

    function getScore(address _user) public view returns (uint256) {
        return scores[_user];
    }
}
