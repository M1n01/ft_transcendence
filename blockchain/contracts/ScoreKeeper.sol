// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract ScoreKeeper {
    mapping(address => uint256) private scores;

    function setScore(uint256 _score) public {
        scores[msg.sender] = _score;
    }

    function getScore(address _address) public view returns (uint256) {
        return scores[_address];
    }
}
