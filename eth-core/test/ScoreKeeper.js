import { expect } from 'chai';
import { describe, it, beforeEach } from 'mocha';
import pkg from 'hardhat';

const { ethers } = pkg;

describe('ScoreKeeper contract', function () {
  let ScoreKeeper;
  let scoreKeeper;
  let owner;

  beforeEach(async function () {
    [owner] = await ethers.getSigners();
    ScoreKeeper = await ethers.getContractFactory('ScoreKeeper');
    scoreKeeper = await ScoreKeeper.deploy(owner.address);
  });

  const addAndVerifyMatch = async (matchId, winner, winnerScore, loser, loserScore) => {
    await scoreKeeper.addMatch(matchId, winner, winnerScore, loser, loserScore);
    const match = await scoreKeeper.getMatch(matchId);
    expect(match.matchId).to.equal(matchId);
    expect(match.winner).to.equal(winner);
    expect(match.winnerScore).to.equal(winnerScore);
    expect(match.loser).to.equal(loser);
    expect(match.loserScore).to.equal(loserScore);
  };

  it('Should add a match correctly', async function () {
    await addAndVerifyMatch(1, 101, 50, 102, 45);
    expect(await scoreKeeper.getMatchCount()).to.equal(1);
  });

  it('Should handle zero scores correctly', async function () {
    await addAndVerifyMatch(1, 103, 0, 104, 0);
  });

  it('Should handle large scores correctly', async function () {
    const largeScore = ethers.MaxUint256;
    await addAndVerifyMatch(2, 105, largeScore, 106, largeScore);
  });

  it('Should handle multiple matches', async function () {
    await addAndVerifyMatch(3, 107, 60, 108, 55);
    await addAndVerifyMatch(4, 109, 70, 110, 65);
  });

  it('Should handle concurrent matches correctly', async function () {
    await Promise.all([
      scoreKeeper.connect(owner).addMatch(6, 111, 80, 112, 75),
      scoreKeeper.connect(owner).addMatch(7, 113, 90, 114, 85),
    ]);

    const match1 = await scoreKeeper.getMatch(6);
    expect(match1.matchId).to.equal(6);
    expect(match1.winner).to.equal(111);
    expect(match1.winnerScore).to.equal(80);
    expect(match1.loser).to.equal(112);
    expect(match1.loserScore).to.equal(75);

    const match2 = await scoreKeeper.getMatch(7);
    expect(match2.matchId).to.equal(7);
    expect(match2.winner).to.equal(113);
    expect(match2.winnerScore).to.equal(90);
    expect(match2.loser).to.equal(114);
    expect(match2.loserScore).to.equal(85);
  });

  it('Should estimate gas usage for adding a match', async function () {
    const tx = await scoreKeeper.addMatch(1, 101, 50, 102, 45);
    const receipt = await tx.wait();
    console.log('Gas used for addMatch:', receipt.gasUsed.toString());
  });

  it('Should revert if called by non-owner', async function () {
    const [owner, nonOwner] = await ethers.getSigners();
    const scoreKeeper = await ScoreKeeper.deploy(owner.address);

    await expect(
      scoreKeeper.connect(nonOwner).addMatch(1, 1, 100, 2, 200)
    ).to.be.revertedWithCustomError(scoreKeeper, 'OwnableUnauthorizedAccount');
  });

  it('Should handle adding multiple matches', async function () {
    const matchesToAdd = 100;
    for (let i = 0; i < matchesToAdd; i++) {
      await scoreKeeper.addMatch(i + 1, i + 101, i + 50, i + 102, i + 45);
    }
    const lastMatch = await scoreKeeper.getMatch(matchesToAdd);
    expect(lastMatch.matchId).to.equal(matchesToAdd);
  });
});
