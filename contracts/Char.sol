pragma solidity 0.8.0;
import "../node_modules/@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "../node_modules/@openzeppelin/contracts/access/Ownable.sol";


interface MyCoin {
function mintTLP(address to,uint256 amount) external;
}


contract Char is ERC721, Ownable {


    struct Face{
        uint8 head;
        uint8 eye;
        uint256 eyebrow;
        uint8 mount;
        uint8 nose;
        uint8 background;
    }

    uint256 nextId = 0;
    uint8 randNonce = 0;

    uint256 fee = 0.002 ether;




    //string fees = 0.002;

    uint attackVictoryProbability = 99;
    mapping ( uint256 => Face) private _tokenDetails;
    address myTokenAddress = 0x0176c767110458dB7eEE8dF1F234bbcFaEfB5900;

    constructor( string memory name, string memory symbol)
    ERC721(name, symbol){}

    function updateFee(uint256 _fee) external onlyOwner(){
        fee = _fee;
    }

    function withdraw() external payable onlyOwner(){
        address payable _owner = payable(owner());
        _owner.transfer(address(this).balance);
    }


   function mintToken(address _to, uint256 _tokenId, string calldata _uri) external onlyOwner {
    _safeMint(_to, _tokenId);
    //super._setTokenUri(_tokenId, _uri);
  }

   mapping (address => uint) balances;


    function sendCoin(address receiver, uint amount)
    public returns(bool success) {
        if (balances[msg.sender] < amount) return false;
        balances[msg.sender] -= amount;
        balances[receiver] += amount;
        emit Transfer(msg.sender, receiver, amount);
        return true;    }

    function mint() public payable {
        uint8 x = 0;
        while (x != 3) {

        uint8 head = 1 ;
        uint8 eye = 1 ;
        uint256 eyebrow = 1 ;
        uint8 mount = 1 ;
        uint8 nose = 1 ;
        uint8 background = 2 ;
        uint ran_number = 0;
        ran_number = randMod(100,3);
        if (ran_number < 50) {head = 2; }
         ran_number = randMod(100,10);
        if (ran_number < 50) {eye = 2; }
         ran_number = randMod(100,18);
        if (ran_number < 50) {eyebrow = 2; }
         ran_number = randMod(100,23);
        if (ran_number < 50) {mount = 2; }
         ran_number = randMod(100,65);
        if (ran_number < 50) {nose = 2; }
         ran_number = randMod(100,55);
        if (ran_number < 85) {background = 1; }

        _tokenDetails[nextId] = Face(head, eye, eyebrow, mount,nose,background);
        _safeMint(msg.sender, nextId);

        nextId++;
        x++;
         }
    }

    function randMod(uint8 _modulus,uint8 number) internal returns(uint256) {

            uint256 ran_n = nextId * 73 * number;
            uint256 abc = uint(keccak256(abi.encodePacked(block.timestamp, msg.sender,ran_n))) % _modulus;
    return abc ;
    }


    // function gift(uint8 damage, uint8 magic, uint256 endurance,address _to) public payable onlyOwner() {
    //     //require(msg.value >= fee );
    //     _tokenDetails[nextId] = Pet(damage, magic, block.timestamp, endurance);
    //     //_safeMint(_to, nextId);
    //     _safeMint(msg.sender, nextId);
    //     nextId++;
    // }

    function feed(uint256 tokenId) public{
            Face storage face = _tokenDetails[tokenId];
            //require(face.lastMeal + face.endurance > block.timestamp);
            //face.eyebrow = block.timestamp;

        }


    //MyCoin public myCoin = new MyCoin("MyCoin","COIN");

    function attack(uint256 tokenId) public payable{
            require(msg.value != fee );
            Face storage face = _tokenDetails[tokenId];
            //require(face.lastMeal + face.endurance > block.timestamp);
            uint rand = randMod(100,99);
            //_mint(msg.sender,1000);
            // if (rand <= attackVictoryProbability) {
            //      face.damage = face.damage +10;
            //      //myCoin.mintTLP(msg.sender,100);
            //     MyCoin(myTokenAddress).mintTLP(msg.sender,22 * 10 ** 18);
            // } else {
            //      face.damage = face.damage -20;
            // }

        }


    function _beforeTokenTransfer(address from, address to, uint256 tokenId) internal override {
                Face storage face = _tokenDetails[nextId];
                // require(face.lastMeal + face.endurance > block.timestamp);
            }

    function getTokenDetails(uint256 tokenId) public view returns (Face memory)
                {
                    return _tokenDetails[tokenId];
                }

    function getAllTokensForUser(address user) public view returns (uint256[] memory){
                    uint256 tokenCount = balanceOf(user);
                    if(tokenCount ==0){
                        return new uint256[](0);

                    }
                    else{
                        uint[] memory result = new uint256[](tokenCount);
                        uint256 totalPets = nextId;
                        uint256 resultIndex = 0;
                        uint256 i;
                        for (i =0; i< totalPets; i++){
                            if(ownerOf(i) == user){
                                result[resultIndex] = i;
                                resultIndex++;
                            }
                        }
                        return result;
                    }

                }
}