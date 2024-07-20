import pkg from 'hardhat';
import process from 'node:process';

const { ethers } = pkg;

async function main() {
  const [deployer] = await ethers.getSigners(); // デプロイ者を取得
  console.log('Deploying contracts with the account:', deployer.address);

  // ScoreKeeperコントラクトをデプロイ
  const scoreKeeper = await ethers.deployContract('ScoreKeeper', [deployer.address]);
  await scoreKeeper.waitForDeployment();
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
