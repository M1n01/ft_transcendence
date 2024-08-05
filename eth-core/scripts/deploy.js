import pkg from 'hardhat';
import process from 'node:process';

const { ethers } = pkg;

async function main() {
  const [deployer] = await ethers.getSigners(); // デプロイ者を取得
  console.log('Deploying contracts with the account:', deployer.address);

  // ScoreKeeperコントラクトをデプロイ
  const scoreKeeper = await ethers.deployContract('ScoreKeeper');
  await scoreKeeper.waitForDeployment();
  console.log('ScoreKeeper deployed to:', scoreKeeper.target);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
