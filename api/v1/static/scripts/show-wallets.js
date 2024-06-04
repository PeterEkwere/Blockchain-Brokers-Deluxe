// show all wallet
let walletDropDown = document.querySelector('wallet-dropdwon')

function dropDownWallets(){
  walletDropDown.classList.toggle('active')
}




// function to handle wallet update

class currencyBox {
  constructor(coinName, coinLogo, holdingBalance, coinBalance){
    this.coinName = coinName
    this.coinLogo = coinLogo
    this.holdingBalance = holdingBalance
    this.coinBalance = coinBalance
  }

}