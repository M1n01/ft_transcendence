const { buildModule } = require('@nomicfoundation/hardhat-ignition/modules');

const PongScoreKeeperModule = buildModule('PongScoreKeeperModule', (m) => {
  const deployer = m.getAccount(0);
  const pongScoreKeeper = m.contract('PongScoreKeeper', [deployer]);

  return { pongScoreKeeper };
});

module.exports = PongScoreKeeperModule;
