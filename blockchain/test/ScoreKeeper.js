import { expect } from 'chai';
import { ethers } from 'hardhat';
import { describe, it } from 'mocha';

describe('ScoreKeeper contarct', function () {
  it('Should set and get the score of an address', async function () {
    const ScoreKeeper = await ethers.getContractFactory('ScoreKeeper');
    const scoreKeeper = await ScoreKeeper.deploy();
    await scoreKeeper.waitForDeployment();

    const [owner] = await ethers.getSigners();
    expect(await scoreKeeper.getScore(owner.address)).to.equal(0);
  });
});
