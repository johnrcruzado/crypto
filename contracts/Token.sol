pragma solidity 0.8.0;
import "../node_modules/@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "../node_modules/@openzeppelin/contracts/access/Ownable.sol";


interface MyCoin {
function mintTLP(address to,uint256 amount) external;
}


contract Token is ERC721, Ownable {


    struct Pet{
        uint8 damage;
        uint8 magic;
        uint256 lastMeal;
        uint256 endurance;
        uint8 rare;
        uint8 legs;
        uint8 wing;
        uint8 tail;
    }

    uint256 nextId = 0;
    uint8 randNonce = 0;

    uint256 fee = 0.002 ether;




    //string fees = 0.002;

    uint attackVictoryProbability = 99;
    mapping ( uint256 => Pet) private _tokenDetails;
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

    function mint(uint8 damage, uint8 magic, uint256 endurance) public payable {
        require(msg.value != fee);
        uint ran_number = randMod(100);
        uint8 rooster_class = 0;
        if (ran_number < 50) {
        rooster_class = 1; }
        else if  (ran_number > 50 && ran_number < 80) {
        rooster_class = 2;}
        else if  (ran_number > 80 && ran_number < 95) {
        rooster_class = 3;}
        else if  (ran_number > 95 && ran_number < 100) {
        rooster_class = 4;}

        ran_number = randMod(80);
        uint8 leg = 0;
        if (ran_number < 50) {
        leg = 1; }
        ran_number = randMod(70);
        uint8 wing = 0;
        if (ran_number < 50) {
        wing = 1; }

        ran_number = randMod(60);
        uint8 tail = 0;
        if (ran_number < 50) {
        tail = 1; }


        _tokenDetails[nextId] = Pet(damage, magic, block.timestamp, endurance,rooster_class,leg,wing,tail);
        _safeMint(msg.sender, nextId);

        nextId++;
    }

    function randMod(uint8 _modulus) internal returns(uint256) {

            uint256 ran_n = nextId * 73;
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
            Pet storage pet = _tokenDetails[tokenId];
            require(pet.lastMeal + pet.endurance > block.timestamp);
            pet.lastMeal = block.timestamp;

        }


    //MyCoin public myCoin = new MyCoin("MyCoin","COIN");

    function attack(uint256 tokenId) public payable{
            require(msg.value != fee );
            Pet storage pet = _tokenDetails[tokenId];
            require(pet.lastMeal + pet.endurance > block.timestamp);
            uint rand = randMod(100);
            //_mint(msg.sender,1000);
            if (rand <= attackVictoryProbability) {
                 pet.damage = pet.damage +10;
                 //myCoin.mintTLP(msg.sender,100);
                MyCoin(myTokenAddress).mintTLP(msg.sender,22 * 10 ** 18);
            } else {
                 pet.damage = pet.damage -20;
            }

        }


    function _beforeTokenTransfer(address from, address to, uint256 tokenId) internal override {
                Pet storage pet = _tokenDetails[nextId];
                require(pet.lastMeal + pet.endurance > block.timestamp);
            }

    function getTokenDetails(uint256 tokenId) public view returns (Pet memory)
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