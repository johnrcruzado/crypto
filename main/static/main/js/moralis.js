Moralis.initialize("eOIBs8NYp3Js2a1g6YSWE0X2MkSb9ljKdpHUfmQf"); // Application id from moralis.io
Moralis.serverURL = "https://guvcyfv1mzqh.moralishost.com:2053/server"; //Server url from moralis.io
//const CONTRACT_ADDRESS = "0xF09C565df1509309a1EfEF2943ef6f3496400651";
const ACCOUNT_ADDRESS = "0xF8D785610411A4268c23746a48148D9e261a5a04";
const TOKEN_ADDRESS = "0x0176c767110458dB7eEE8dF1F234bbcFaEfB5900";
const CONTRACT_ADDRESS = "0x76C1fb7A3a7313A67cE56479321Ad6C77AfAB721";

async function init() {
    try {
        let user = Moralis.User.current();
        console.log(user);
        if(!user){
            $("#login_button").click ( () => {
            user = Moralis.Web3.authenticate();
            alert("User Logged in");
            })

        }
        else{
         renderGame();
         }
    } catch (error) {
        console.log(error);
    }
}

async function renderGame(){
    $("#login_button").hide();
    $("#pet_row").html("");
    let petId = 0;
    const accounts = await ethereum.request({ method: 'eth_accounts' });
    console.log(accounts);
    window.web3 = await Moralis.Web3.enable();
    let abi = await getAbi();
    let contract = new web3.eth.Contract(abi,CONTRACT_ADDRESS);
    let array = await contract.methods.getAllTokensForUser(ethereum.selectedAddress).call({from : ethereum.selectedAddress})
    console.log(array)
    if(array.length == 0) return;
    array.forEach(async (petId) => {
        let details = await contract.methods.getTokenDetails(petId).call({from: ethereum.selectedAddress});
        renderPet(petId,details);
    })

    //let data = await contract.methods.getTokenDetails(petId).call({from : ethereum.selectAddress})
    //renderPet(0,data)
    //console.log(data);
}

function renderPet(id,data){

    let deathTime = new Date( (parseInt(data.lastMeal) + parseInt(data.endurance))* 1000);
    let now = new Date();
    if(now > deathTime){
        deathTime = "<b>DEAD</b>"
    }
    html_image =''
    if (data.background == 1){ html_image += `<img src="/static/main/img/face/background_1.png" class="fishes" style="width: 350px;height: 350px"/>`}
    else{html_image += `<img src="/static/main/img/face/background_3.png" class="fishes" style="width: 350px;height: 350px"/>` }

    html_image += `<img src="/static/main/img/face/blank_face.png" class="fish" style="width: 350px;height: 350px"/>`

    if (data.head == 2){ html_image += `<img src="/static/main/img/face/hair_2.png" class="fish" style="width: 350px;height: 350px"/>`}
    else{html_image += `<img src="/static/main/img/face/hair_1.png" class="fish" style="width: 350px;height: 350px"/>` }

    if (data.eyebrow == 2){ html_image += `<img src="/static/main/img/face/eyebrow_2.png" class="fish" style="width: 350px;height: 350px"/>`}
    else{html_image += `<img src="/static/main/img/face/eyebrow_1.png" class="fish" style="width: 350px;height: 350px"/>` }

    if (data.eye == 2){ html_image += `<img src="/static/main/img/face/eye_2.png" class="fish" style="width: 350px;height: 350px"/>`}
    else{html_image += `<img src="/static/main/img/face/eye_1.png" class="fish" style="width: 350px;height: 350px"/>` }

    if (data.nose == 2){ html_image += `<img src="/static/main/img/face/nose_2.png" class="fish" style="width: 350px;height: 350px"/>`}
    else{html_image += `<img src="/static/main/img/face/nose_1.png" class="fish" style="width: 350px;height: 350px"/>` }

    if (data.mount == 2){ html_image += `<img src="/static/main/img/face/mount_2.png" class="fish" style="width: 350px;height: 350px"/>`}
    else{html_image += `<img src="/static/main/img/face/mount_1.png" class="fish" style="width: 350px;height: 350px"/>` }

    let htmlString = `<div id="pet_${id}" ><div style="float: left;margin-left: 30px"><div style="position: relative; left: 0; top: 0;"> 
                ${html_image}
                <div>ID: <span id="${id}"></span>${id}</div>
                <div>DA: <span ></span>${data.head} ${data.eyebrow} ${data.eye} ${data.nose}  ${data.mount} ${data.background} </div>
                <div>Time to starvation: <span >${deathTime}</span></div>
                <button data-pet-id="${id}"  class="feed_button btn btn-primary btn-block">Feed</button>
                <button data-pet-id="${id}"  class="attack_button btn btn-primary btn-block">Attack</button>
            </div></div></div>`;



    let element = $.parseHTML(htmlString);
    $("#pet_row").append(element);

    $(`#pet_${id} .feed_button`).click(() => {
    feed(id);})

    $(`#pet_${id} .attack_button`).click(() => {
    attack(id);})
}

function getAbi(){
    return new Promise((res) =>{
        //$.getJSON("/static/main/js/Token.json", ( (json)
        $.getJSON("/static/main/js/Char.json", ( (json) =>
        {
            res(json.abi);

        }))
    })
}


function getAbiTalpak(){
    return new Promise((res) =>{
        $.getJSON("/static/main/js/Talpak.json", ( (json) =>
        {
            res(json.abi);

        }))
    })
}

async function feed(petId){
    let abi = await getAbi();
    let contract = new web3.eth.Contract(abi,CONTRACT_ADDRESS);
    contract.methods.feed(petId).send({from: ethereum.selectedAddress}).on("receipt",( () => {
        console.log("done");
    }))
}

async function attack(petId){
    let abi = await getAbi();
    let contract = new web3.eth.Contract(abi,CONTRACT_ADDRESS);
    contract.methods.attack(petId).send({from: ethereum.selectedAddress}).on("receipt",( () => {
        console.log("done");
    }))

    // let abiTalak = await getAbiTalpak();
    //
    // let talpak = new web3.eth.Contract(abiTalak,TOKEN_ADDRESS);
    // talpak.methods.mintToken("0xB8cc1AcA33eB5646A575f03B67E3d291f3540972",200).send({from: ethereum.selectedAddress}).on("receipt",( () => {
    //     console.log("done");
    // }))
}


async function hatch(){
    let abi = await getAbi();
    let contract = new web3.eth.Contract(abi,CONTRACT_ADDRESS);
    // contract.methods.mint(100,200,10000).send({from: ethereum.selectedAddress}).on("receipt",( () => {
    //     console.log("done");
    // }))
    contract.methods.mint().send({from: ethereum.selectedAddress}).on("receipt",( () => {
    console.log("done");
    }))


}

$("#hatch_btn").click( () =>
{
    console.log("hatch_btn");
    hatch();
});

    //function mint(uint8 damage, uint8 magic, uint256 endurance) public onlyOwner {
    //    _tokenDetails[nextId] = Pet(damage, magic, block.timestamp, endurance);
    //    _safeMint(msg.sender, nextId);
    //    nextId++;
    //}
    //function feed(uint256 tokenId) public{
    //    Pet storage pet = _tokenDetails[tokenId];
    //    require(pet.lastMeal + pet.endurance > block.timestamp);
    //    pet.lastMeal = block.timestamp;
    //}




init();

