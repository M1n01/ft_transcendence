require('@nomicfoundation/hardhat-toolbox');
require('dotenv').config();
const process = require('process');

module.exports = {
  solidity: '0.8.24',
  networks: {
    hardhat: {
      chainId: 1337,
    },
    sepolia: {
      url: process.env.PROVIDER_URL || "",
      accounts: process.env.SEPOLIA_ACCOUNTS ? [process.env.SEPOLIA_ACCOUNTS] : [] // 環境変数からアカウントを取得
    },
  },
};
