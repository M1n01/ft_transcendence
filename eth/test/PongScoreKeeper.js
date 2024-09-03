import { expect } from 'chai';
import { describe, it, beforeEach } from 'mocha';
import pkg from 'hardhat';

const { ethers } = pkg;

describe('PongScoreKeeper contract', function () {
  let PongScoreKeeper;
  let pongScoreKeeper;
  let owner;

  beforeEach(async function () {
    [owner] = await ethers.getSigners();
    PongScoreKeeper = await ethers.getContractFactory('PongScoreKeeper');
    pongScoreKeeper = await PongScoreKeeper.deploy(owner.address);
    await pongScoreKeeper.waitForDeployment();
  });

  const addAndVerifyMatch = async (winner, winnerScore, loser, loserScore) => {
    await pongScoreKeeper.createMatch(
      BigInt(winner),
      BigInt(winnerScore),
      BigInt(loser),
      BigInt(loserScore)
    );
    const matchId = (await pongScoreKeeper.nextMatchId()) - 1n;
    const match = await pongScoreKeeper.getMatch(matchId);
    expect(match.winner).to.equal(BigInt(winner));
    expect(match.winnerScore).to.equal(BigInt(winnerScore));
    expect(match.loser).to.equal(BigInt(loser));
    expect(match.loserScore).to.equal(BigInt(loserScore));
  };

  it('Should add a match correctly', async function () {
    await addAndVerifyMatch(101, 50, 102, 45);
    expect(await pongScoreKeeper.getMatchCount()).to.equal(1n);
  });

  it('Should handle zero scores correctly', async function () {
    await addAndVerifyMatch(103, 0, 104, 0);
  });

  it('Should handle large scores correctly', async function () {
    const largeScore = 32767; // int16の最大値
    await addAndVerifyMatch(105, largeScore, 106, largeScore);
  });

  it('Should handle multiple matches', async function () {
    await addAndVerifyMatch(107, 60, 108, 55);
    await addAndVerifyMatch(109, 70, 110, 65);
  });

  it('Should estimate gas usage for adding a match', async function () {
    const tx = await pongScoreKeeper.createMatch(101, 50, 102, 45);
    const receipt = await tx.wait();
    console.log('Gas used for createMatch:', receipt.gasUsed.toString());
  });

  it('Should revert if called by non-owner', async function () {
    const [owner, nonOwner] = await ethers.getSigners();
    const pongScoreKeeper = await PongScoreKeeper.deploy(owner.address);

    await expect(
      pongScoreKeeper.connect(nonOwner).createMatch(1, 100, 2, 200)
    ).to.be.revertedWithCustomError(pongScoreKeeper, 'OwnableUnauthorizedAccount');
  });
});
