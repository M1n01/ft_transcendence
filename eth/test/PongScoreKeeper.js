import { expect } from 'chai';
import { describe, it, beforeEach } from 'mocha';
import { time } from '@nomicfoundation/hardhat-network-helpers';
import pkg from 'hardhat';
import { v4 as uuidv4 } from 'uuid';

const { ethers } = pkg;
const { utils } = ethers;

describe('PongScoreKeeper contract', function () {
  let PongScoreKeeper;
  let pongScoreKeeper;
  let owner;
  let addr1;
  const user1 = utils.formatBytes16String(uuidv4());
  const user2 = utils.formatBytes16String(uuidv4());
  const user3 = utils.formatBytes16String(uuidv4());
  const tournamentId = utils.formatBytes16String(uuidv4());

  beforeEach(async function () {
    [owner, addr1] = await ethers.getSigners();
    PongScoreKeeper = await ethers.getContractFactory('PongScoreKeeper');
    pongScoreKeeper = await PongScoreKeeper.deploy();
    await pongScoreKeeper.waitForDeployment();
  });

  describe('Deployment', function () {
    it('Should set the right owner', async function () {
      expect(await pongScoreKeeper.owner()).to.equal(owner.address);
    });

    it('Should start with nextMatchId as 1', async function () {
      expect(await pongScoreKeeper.nextMatchId()).to.equal(0);
    });
  });

  describe('Match Creation', function () {
    it('Should create a match correctly', async function () {
      await pongScoreKeeper.createMatch(tournamentId, user1, 11, user2, 5, 1);
      const match = await pongScoreKeeper.getMatch(0, true);
      expect(match.tournamentId).to.equal(tournamentId);
      expect(match.player1).to.equal(user1);
      expect(match.player2).to.equal(user2);
      expect(match.player1Score).to.equal(11);
      expect(match.player2Score).to.equal(5);
      expect(match.isActive).to.be.true;
      expect(match.round).to.equal(1);
    });

    it('Should fail if player1 and player2 are the same', async function () {
      await expect(
        pongScoreKeeper.createMatch(tournamentId, user1, 11, user1, 5, 1)
      ).to.be.revertedWith('player1 and player2 cannot be the same');
    });

    it('Should emit MatchCreated event', async function () {
      await expect(pongScoreKeeper.createMatch(tournamentId, user1, 11, user2, 5, 2))
        .to.emit(pongScoreKeeper, 'MatchCreated')
        .withArgs(0, tournamentId, await time.latest(), user1, user2, 2);
    });

    it('Should fail if caller is not the owner', async function () {
      await expect(pongScoreKeeper.connect(owner).createMatch(tournamentId, user1, 11, user2, 5, 3))
        .to.be.reverted;
    });

    // 境界値テスト
    it('Should create a match with minimum winning score difference', async function () {
      await expect(pongScoreKeeper.createMatch(tournamentId, user1, 11, user2, 10, 4)).to.not.be
        .reverted;
    });

    it('Should create a match with maximum possible scores', async function () {
      await expect(pongScoreKeeper.createMatch(tournamentId, user1, 65535, user2, 65534, 5)).to.not
        .be.reverted;
    });
  });

  describe('Match Retrieval', function () {
    beforeEach(async function () {
      await pongScoreKeeper.createMatch(tournamentId, user1, 11, user2, 5, 1);
      await pongScoreKeeper.createMatch(tournamentId, user2, 11, user1, 7, 1);
    });

    it('Should retrieve a single match correctly', async function () {
      const match = await pongScoreKeeper.getMatch(0, true);
      expect(match.player1).to.equal(user1);
    });

    it('Should fail to retrieve a non-existent match', async function () {
      await expect(pongScoreKeeper.getMatch(3, true)).to.be.revertedWith('Match not found');
    });

    it('Should retrieve all matches correctly', async function () {
      const matches = await pongScoreKeeper.getAllMatches(false);
      expect(matches.length).to.equal(2);
    });
  });

  describe('Match Status Toggle', function () {
    beforeEach(async function () {
      await pongScoreKeeper.createMatch(tournamentId, user1, 11, user2, 5, 1);
    });

    it('Should toggle match status correctly', async function () {
      await pongScoreKeeper.deleteMatch(0);
      await expect(pongScoreKeeper.getMatch(0, true)).to.be.revertedWith('Match not found');
    });

    it('Should fail to toggle status of a non-existent match', async function () {
      await expect(pongScoreKeeper.deleteMatch(3)).to.be.revertedWith('Match not found');
    });

    it('Should emit MatchStatusChanged event', async function () {
      await expect(pongScoreKeeper.deleteMatch(0))
        .to.emit(pongScoreKeeper, 'MatchStatusChanged')
        .withArgs(0, false);
    });
  });

  describe('Gas Optimization', function () {
    it('Should optimize gas usage for match creation', async function () {
      const tx = await pongScoreKeeper.createMatch(tournamentId, user1, 11, user2, 5, 1);
      const receipt = await tx.wait();
      expect(receipt.gasUsed).to.be.below(200000); // 適切なガス制限を設定
    });
  });

  describe('Security', function () {
    it('Should not allow non-owners to create matches', async function () {
      await expect(pongScoreKeeper.connect(addr1).createMatch(tournamentId, user2, 11, user3, 5, 1))
        .to.be.reverted;
    });
  });
});
