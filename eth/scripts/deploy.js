import pkg from 'hardhat';
import process from 'node:process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const { ethers } = pkg;
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

async function main() {
  const [deployer] = await ethers.getSigners(); // デプロイ者を取得
  console.log('Deploying contracts with the account:', deployer.address);

  // ScoreKeeperコントラクトをデプロイ
  const ScoreKeeper = await ethers.getContractFactory('PongScoreKeeper');
  const scoreKeeper = await ScoreKeeper.deploy(deployer.address);
  await scoreKeeper.waitForDeployment();

  const addressPath = path.resolve(__dirname, '../contract_address.txt');
  fs.writeFileSync(addressPath, scoreKeeper.target);
  console.log('PongScoreKeeper deployed to:', scoreKeeper.target);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
