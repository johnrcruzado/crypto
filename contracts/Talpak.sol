pragma solidity 0.8.0;

//import 'https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol';
import "../node_modules/@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Talpak is ERC20 {
    address admin = 0xF8D785610411A4268c23746a48148D9e261a5a04;


    constructor( string memory name, string memory symbol)
    ERC20(name, symbol){
        _mint(msg.sender, 10000 * 10 ** 18);
        _mint(0xB8cc1AcA33eB5646A575f03B67E3d291f3540972, 10000 * 10 ** 18);
    }

    // function mintTaplak(address to, uint amount) internal virtual {
    //     //require(msg.sender == admin, 'only admin');
    //     _mint(to, amount);
    // }

    function mintTLP(address account, uint256 amount) public {
    _mint(account, amount);
    }



    function burnTaplak(uint amount )external{
        _burn(msg.sender, amount) ;
    }

}