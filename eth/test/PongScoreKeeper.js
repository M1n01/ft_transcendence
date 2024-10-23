import { expect } from 'chai';
import { describe, it, beforeEach } from 'mocha';
import { time } from '@nomicfoundation/hardhat-network-helpers';
import pkg from 'hardhat';

const { ethers } = pkg;

describe('PongScoreKeeper contract', function () {
  let PongScoreKeeper;
  let pongScoreKeeper;
  let owner;
  let addr1;

  function uuidToBytes16(uuid) {
    // Remove hyphens and convert to lowercase
    const hex = uuid.replace(/-/g, '').toLowerCase();
    // Pad with zeros if necessary (shouldn't be needed for valid UUIDs)
    const paddedHex = hex.padStart(32, '0');
    // Prefix with '0x' to create a valid hex string
    return '0x' + paddedHex;
  }

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
  });

  describe('Match Creation', function () {
    const player1 = uuidToBytes16(crypto.randomUUID());
    const player2 = uuidToBytes16(crypto.randomUUID());

    it('Should create a match correctly', async function () {
      const matchId = uuidToBytes16(crypto.randomUUID());
      const tournamentId = uuidToBytes16(crypto.randomUUID());

      await pongScoreKeeper.createMatch(matchId, tournamentId, player1, player2, 15, 3, 1);

      const match = await pongScoreKeeper.getMatch(matchId, true);
      expect(match.player1).to.equal(player1);
      expect(match.player2).to.equal(player2);
      expect(match.tournamentId).to.equal(tournamentId);
    });

    it('Should fail if player1 and player2 are the same', async function () {
      const matchId = uuidToBytes16(crypto.randomUUID());
      const tournamentId = uuidToBytes16(crypto.randomUUID());
      const player3 = player1;

      await expect(
        pongScoreKeeper.createMatch(matchId, tournamentId, player1, player3, 15, 5, 1)
      ).to.be.revertedWith('player1 and player2 cannot be the same');
    });

    it('Should emit MatchCreated event', async function () {
      const matchId = uuidToBytes16(crypto.randomUUID());
      const tournamentId = uuidToBytes16(crypto.randomUUID());

      await expect(pongScoreKeeper.createMatch(matchId, tournamentId, player1, player2, 15, 5, 2))
        .to.emit(pongScoreKeeper, 'MatchCreated')
        .withArgs(matchId, tournamentId, await time.latest(), player1, player2, 2);
    });

    it('Should fail if caller is not the owner', async function () {
      const matchId = uuidToBytes16(crypto.randomUUID());
      const tournamentId = uuidToBytes16(crypto.randomUUID());

      await expect(
        pongScoreKeeper
          .connect(addr1)
          .createMatch(matchId, tournamentId, player1, player2, 15, 5, 3)
      ).to.be.reverted;
    });

    // 境界値テスト
    it('Should create a match with minimum winning score difference', async function () {
      const matchId = uuidToBytes16(crypto.randomUUID());
      const tournamentId = uuidToBytes16(crypto.randomUUID());

      await expect(pongScoreKeeper.createMatch(matchId, tournamentId, player1, player2, 15, 10, 4))
        .to.not.be.reverted;
    });

    it('Should create a match with maximum possible scores', async function () {
      const matchId = uuidToBytes16(crypto.randomUUID());
      const tournamentId = uuidToBytes16(crypto.randomUUID());

      await expect(
        pongScoreKeeper.createMatch(matchId, tournamentId, player1, player2, 65535, 65534, 5)
      ).to.not.be.reverted;
    });
  });

  describe('Match Retrieval', function () {
    const matchId = uuidToBytes16(crypto.randomUUID());
    const matchId2 = uuidToBytes16(crypto.randomUUID());
    const player1 = uuidToBytes16(crypto.randomUUID());
    const player2 = uuidToBytes16(crypto.randomUUID());

    beforeEach(async function () {
      const tournamentId = uuidToBytes16(crypto.randomUUID());

      await pongScoreKeeper.createMatch(matchId, tournamentId, player1, player2, 15, 5, 1);
      await pongScoreKeeper.createMatch(matchId2, tournamentId, player2, player1, 15, 7, 1);
    });

    it('Should retrieve a single match correctly', async function () {
      const match = await pongScoreKeeper.getMatch(matchId, true);
      expect(match.player1).to.equal(player1);
    });

    it('Should fail to retrieve a non-existent match', async function () {
      const nonExistentMatchId = uuidToBytes16(crypto.randomUUID());
      await expect(pongScoreKeeper.getMatch(nonExistentMatchId, true)).to.be.revertedWith(
        'Match not found'
      );
    });

    it('Should retrieve all matches correctly', async function () {
      const matches = await pongScoreKeeper.getAllMatches(false);
      expect(matches.length).to.equal(2);
    });
  });

  describe('Match Status Toggle', function () {
    const matchId = uuidToBytes16(crypto.randomUUID());

    beforeEach(async function () {
      const tournamentId = uuidToBytes16(crypto.randomUUID());
      const player1 = uuidToBytes16(crypto.randomUUID());
      const player2 = uuidToBytes16(crypto.randomUUID());

      await pongScoreKeeper.createMatch(matchId, tournamentId, player1, player2, 15, 5, 1);
    });

    it('Should toggle match status correctly', async function () {
      await pongScoreKeeper.deleteMatch(matchId);
      await expect(pongScoreKeeper.getMatch(matchId, true)).to.be.revertedWith('Match not found');
    });

    it('Should fail to toggle status of a non-existent match', async function () {
      const nonExistentMatchId = uuidToBytes16(crypto.randomUUID());
      await expect(pongScoreKeeper.deleteMatch(nonExistentMatchId)).to.be.revertedWith(
        'Match not found'
      );
    });

    it('Should emit MatchStatusChanged event', async function () {
      await expect(pongScoreKeeper.deleteMatch(matchId))
        .to.emit(pongScoreKeeper, 'MatchStatusChanged')
        .withArgs(matchId, false);
    });
  });

  describe('Gas Optimization', function () {
    it('Should optimize gas usage for match creation', async function () {
      const matchId = uuidToBytes16(crypto.randomUUID());
      const tournamentId = uuidToBytes16(crypto.randomUUID());
      const player1 = uuidToBytes16(crypto.randomUUID());
      const player2 = uuidToBytes16(crypto.randomUUID());

      const tx = await pongScoreKeeper.createMatch(
        matchId,
        tournamentId,
        player1,
        player2,
        15,
        5,
        1
      );
      const receipt = await tx.wait();
      expect(receipt.gasUsed).to.be.below(200000); // 適切なガス制限を設定
    });
  });

  describe('Security', function () {
    it('Should not allow non-owners to create matches', async function () {
      const matchId = uuidToBytes16(crypto.randomUUID());
      const tournamentId = uuidToBytes16(crypto.randomUUID());
      const player1 = uuidToBytes16(crypto.randomUUID());
      const player2 = uuidToBytes16(crypto.randomUUID());

      await expect(
        pongScoreKeeper
          .connect(addr1)
          .createMatch(matchId, tournamentId, player1, player2, 15, 5, 1)
      ).to.be.reverted;
    });
  });
});
