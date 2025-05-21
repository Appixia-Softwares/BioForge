const hre = require("hardhat")

async function main() {
  // Deploy the BioForgeIPNFT contract
  const BioForgeIPNFT = await hre.ethers.getContractFactory("BioForgeIPNFT")
  const bioForgeIPNFT = await BioForgeIPNFT.deploy()

  await bioForgeIPNFT.deployed()

  console.log("BioForgeIPNFT deployed to:", bioForgeIPNFT.address)
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error)
    process.exit(1)
  })
