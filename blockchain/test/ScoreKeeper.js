import { expect } from 'chai';
import { describe, it } from 'mocha';
import { ethers } from 'hardhat';

describe('ScoreKeeper contarct', function () {
  it('Should set and get the score of an address', async function () {
    const [owner, otherAccount] = await ethers.getSigners();
    const ScoreKeeper = await ethers.getContractFactory('ScoreKeeper');
    const scoreKeeper = await ScoreKeeper.deploy(owner.address);
    await scoreKeeper.waitForDeployment();

    await scoreKeeper.setScore(owner.address, 100);
    expect(await scoreKeeper.getScore(owner.address)).to.equal(100);

    await scoreKeeper.setScore(otherAccount.address, 200);
    expect(await scoreKeeper.getScore(otherAccount.address)).to.equal(200);

    await expect(scoreKeeper.connect(otherAccount).setScore(owner.address, 300)).to.be.revertedWith(
      'Ownable: caller is not the owner'
    );
  });
});
