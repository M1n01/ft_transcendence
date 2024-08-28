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
    await scoreKeeper.waitForDeployment();
  });

  const addAndVerifyMatch = async (winner, winnerScore, loser, loserScore) => {
    await scoreKeeper.createGame(
      BigInt(winner),
      BigInt(winnerScore),
      BigInt(loser),
      BigInt(loserScore)
    );
    const matchId = (await scoreKeeper.nextGameId()) - 1n;
    const match = await scoreKeeper.getGame(matchId);
    expect(match.winner).to.equal(BigInt(winner));
    expect(match.winnerScore).to.equal(BigInt(winnerScore));
    expect(match.loser).to.equal(BigInt(loser));
    expect(match.loserScore).to.equal(BigInt(loserScore));
  };

  it('Should add a match correctly', async function () {
    await addAndVerifyMatch(101, 50, 102, 45);
    expect(await scoreKeeper.getGameCount()).to.equal(1n);
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

  // it('Should handle concurrent matches correctly', async function () {
  //   await Promise.all([
  //     scoreKeeper.connect(owner).createGame(111, 80, 112, 75),
  //     scoreKeeper.connect(owner).createGame(113, 90, 114, 85),
  //   ]);

  //   const match1 = await scoreKeeper.getGame(6);
  //   expect(match1.matchId).to.equal(6);
  //   expect(match1.winner).to.equal(111);
  //   expect(match1.winnerScore).to.equal(80);
  //   expect(match1.loser).to.equal(112);
  //   expect(match1.loserScore).to.equal(75);

  //   const match2 = await scoreKeeper.getGame(7);
  //   expect(match2.matchId).to.equal(7);
  //   expect(match2.winner).to.equal(113);
  //   expect(match2.winnerScore).to.equal(90);
  //   expect(match2.loser).to.equal(114);
  //   expect(match2.loserScore).to.equal(85);
  // });

  it('Should estimate gas usage for adding a match', async function () {
    const tx = await scoreKeeper.createGame(101, 50, 102, 45);
    const receipt = await tx.wait();
    console.log('Gas used for createGame:', receipt.gasUsed.toString());
  });

  it('Should revert if called by non-owner', async function () {
    const [owner, nonOwner] = await ethers.getSigners();
    const scoreKeeper = await ScoreKeeper.deploy(owner.address);

    await expect(
      scoreKeeper.connect(nonOwner).createGame(1, 100, 2, 200)
    ).to.be.revertedWithCustomError(scoreKeeper, 'OwnableUnauthorizedAccount');
  });

  // it('Should handle adding multiple matches', async function () {
  //   const matchesToAdd = 100;
  //   for (let i = 0; i < matchesToAdd; i++) {
  //     await scoreKeeper.createGame(i + 101, i + 50, i + 102, i + 45);
  //   }
  //   const lastMatch = await scoreKeeper.getGame(matchesToAdd);
  //   expect(lastMatch.winner).to.equal(matchesToAdd + 101);
  //   expect(lastMatch.winnerScore).to.equal(matchesToAdd + 50);
  //   expect(lastMatch.loser).to.equal(matchesToAdd + 102);
  //   expect(lastMatch.loserScore).to.equal(matchesToAdd + 45);
  // });
});
