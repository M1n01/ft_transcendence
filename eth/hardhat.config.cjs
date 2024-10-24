require('@nomicfoundation/hardhat-toolbox');
require('dotenv').config({ path: '../.env' });
const process = require('process');

module.exports = {
  solidity: {
    version: '0.8.24',
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
    },
  },
  networks: {
    hardhat: {
      chainId: 1337,
    },
    sepolia: {
      url: process.env.PROVIDER_URL || '',
      accounts:
        process.env.PRIVATE_ACCOUNT_KEY !== undefined ? [process.env.PRIVATE_ACCOUNT_KEY] : [],
    },
  },
};
