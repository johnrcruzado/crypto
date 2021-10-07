//const Token = artifacts.require("Token");
//const Talpak = artifacts.require("MyCoin");
const Char = artifacts.require("Char");

module.exports = async function (deployer) {
  //await deployer.deploy(Token, "MyCoin", "COIN");
  //await deployer.deploy(Talpak, "MyCoin", "COIN");
  //let tokenInstance = await Token.deployed();
  //let tokenTalpak = await Talpak.deployed();
  //await tokenInstance.mint(33,200, 10000);
  //await tokenInstance.mint(150,150, 10000);
  //let pet = await tokenInstance.getTokenDetails(1);
  //await tokenInstance.attack(0);
  //tokenTalpak.mintToken("0xF8D785610411A4268c23746a48148D9e261a5a04",55)

  await deployer.deploy(Char, "CHAR", "CHR");
  let tokenInstance = await Char.deployed();
};
