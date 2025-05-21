/**
 * @type import('hardhat/config').HardhatUserConfig
 */

// Hardhat configuration file
// This uses CommonJS module syntax as required by Hardhat
const { task } = require("hardhat/config")
require("@nomicfoundation/hardhat-toolbox")
require("dotenv").config()

// Default to empty string if environment variables are not set
const POLYGON_RPC_URL = process.env.POLYGON_RPC_URL || "https://polygon-rpc.com"
const MUMBAI_RPC_URL = process.env.MUMBAI_RPC_URL || "https://rpc-mumbai.maticvigil.com"
const PRIVATE_KEY = process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : []
const POLYGONSCAN_API_KEY = process.env.POLYGONSCAN_API_KEY || ""

// Export the Hardhat configuration
module.exports = {
  solidity: "0.8.18",
  networks: {
    hardhat: {},
    polygon: {
      url: POLYGON_RPC_URL,
      accounts: PRIVATE_KEY,
    },
    mumbai: {
      url: MUMBAI_RPC_URL,
      accounts: PRIVATE_KEY,
    },
  },
  etherscan: {
    apiKey: POLYGONSCAN_API_KEY,
  },
}
