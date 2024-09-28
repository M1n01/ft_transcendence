import pkg from 'hardhat';
const { ethers } = pkg;
import dotenv from 'dotenv';
import process from 'node:process';

dotenv.config();

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log('Deploying contracts with the account:', await deployer.getAddress());

  // ScoreKeeperコントラクトをデプロイ
  const PongScoreKeeper = await ethers.getContractFactory('PongScoreKeeper');
  const pongScoreKeeper = await PongScoreKeeper.deploy(await deployer.getAddress());
  await pongScoreKeeper.waitForDeployment();

  console.log('PongScoreKeeper deployed to:', await pongScoreKeeper.target);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
