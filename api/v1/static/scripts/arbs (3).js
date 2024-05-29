document.addEventListener("DOMContentLoaded", function () {
  var header = document.querySelector("header");

  window.addEventListener("scroll", function () {
    if (window.scrollY > 0) {
      header.style.boxShadow = "0px 2px 5px rgba(0, 0, 0, 0.1)";
    } else {
      header.style.boxShadow = "none";
    }
  });
});


window.addEventListener('load', () => {
  const body = document.querySelector('body');
  body.style.visibility = 'hidden';

  setTimeout(() => {
    body.style.visibility = 'visible';
  }, 0);

  let isNavOpen = false;
  const toggleBtn = document.getElementById('toggleBtn');
  const mySidepanel = document.getElementById('mySidepanel');

  toggleBtn.addEventListener('click', (event) => {
    event.stopPropagation();
    isNavOpen ? closeNav() : openNav();
  });

  function openNav() {
    closeFilter()
    mySidepanel.style.width = "200";
    body.style.overflowY = "hidden";
    isNavOpen = true;

    document.addEventListener('click', closeNavOutside);
    toggleBtn.classList.add('active');
  }

  function closeNav() {
    if (window.innerWidth < 1000) {
      mySidepanel.style.width = "0";
    } else {
      document.querySelector('nav').style.width = "fit-content";
    }
    body.style.overflowY = "auto";
    isNavOpen = false;

    document.removeEventListener('click', closeNavOutside);
    toggleBtn.classList.remove('active');
  }

  function closeNavOutside(event) {
    if (!mySidepanel.contains(event.target) && event.target !== toggleBtn) {
      closeNav();
    }
  }

  let isFilterOpen = false;
  const filterBtn = document.getElementById('filterBtn');
  const filterPage = document.getElementById('filter-page');
  const filterbox = document.getElementById('filterBox');

  filterBtn.addEventListener('click', (event) => {
    event.stopPropagation();
    isFilterOpen ? closeFilter() : openFilter();
  });

  function openFilter() {
    closeNav(); // Close the side panel if it's open
    filterPage.style.width = '150px'
    filterPage.style.height = '100%'
    filterPage.style.visibility = 'visible'
    filterbox.style.display ='block'
    
    if(window.innerWidth > 900){
      body.style.marginRight = '70px'
    }

    if(window.innerWidth < 500){
      filterPage.style.right = ''
      filterPage.style.left = '0'
    } else{
      filterPage.style.right = '0'
      filterPage.style.left = ''
    }

    isFilterOpen = true;

    document.addEventListener('click', closeFilterOutside);
  }

 

  function closeFilter() {

    filterPage.style.width = '0';
    filterbox.style.transition ='0.3s'
    filterbox.style.display = 'none'
    isFilterOpen = false;
    filterPage.style.visibility = 'hidden'
    body.style.marginRight = ''


    document.removeEventListener('click', closeFilterOutside);
  }


  

  function closeFilterOutside(event) {
    if (!filterPage.contains(event.target) && event.target !== filterBtn) {
      closeFilter();
    }
  }

  
  

  // Add a global click event listener to close both the side panel and filter
  document.addEventListener('click', (event) => {
    const isInsideFilterPage = filterPage.contains(event.target) || filterBtn.contains(event.target);
    const isInsideSidePanel = mySidepanel.contains(event.target) || toggleBtn.contains(event.target);

    if (!isInsideFilterPage && !isInsideSidePanel) {
      closeNav();
      closeFilter();
    }
  });

  // Add a resize event listener to handle changes in window width
  window.addEventListener('resize', () => {
    if (isFilterOpen) {
      closeFilter();
      openFilter();
    }
  });
});



  window.addEventListener('resize', function () {
    var sidepanel = document.getElementById("mySidepanel");
    var openBtn = document.getElementById("openBtn");
    var closeBtn = document.getElementById("closeBtn");
    var freeBtn1 = document.querySelector(".freebtn1");
    var hamDiv = document.getElementById('hamDiv');

    if (window.innerWidth > 1000) {
        sidepanel.classList.add("open");
        sidepanel.style.opacity = "1";
        sidepanel.style.width = "auto";
        openBtn.style.display = "none";
        closeBtn.style.display = "none";
        freeBtn1.style.display = "block";
    }

    if (this.window.innerWidth <= 1000){
      sidepanel.classList.remove("open");
      sidepanel.style.width = "0";
      openBtn.style.display = "inline";
      closeBtn.style.display = "none";
      freeBtn1.style.display = "none";
      document.getElementById("nav-links").style.display = "none"
    }

    
});





const images = document.querySelectorAll('.arrow-icon');
const smallScreenSrc = "img/icons8-expand-arrow-26.png";

function handleMediaQueryChange(mediaQuery) {
    images.forEach((image) => {
        if (mediaQuery.matches) {
            // Change image source for small screens
            image.src = smallScreenSrc;
        } else {
            // Reset to the original source for larger screens
            image.src = 'img/icons8-expand-arrow-24.png';
        }
    });
}

const mediaQuery = window.matchMedia('(max-width: 1000px)');
handleMediaQueryChange(mediaQuery); // Initial check
mediaQuery.addListener(handleMediaQueryChange);

var navDropDowns = document.querySelectorAll('.dp-a');



function toggleDropdown(dropdownId) {
  var navDd = document.getElementById(dropdownId + '-content');
  navDd.classList.toggle('active');
}

function rotateArrowIcon(arrowId) {
  let arrow = document.getElementById(arrowId);
  let currentRotation = arrow.style.transform.replace('rotate(', '').replace('deg)', '');

  if (currentRotation === '180') {
    arrow.style.transform = 'rotate(0deg)';
  } else {
    arrow.style.transform = 'rotate(180deg)';
  }
}








    document.addEventListener("DOMContentLoaded", function() {
        var avatar = document.getElementById("avatar-img");

        avatar.addEventListener("click", function() {
            var input = document.createElement("input");
            input.type = "file";
            input.accept = "image/*";
            input.onchange = function(event) {
                var file = event.target.files[0];
                var reader = new FileReader();
                reader.onload = function(e) {
                    avatar.src = e.target.result;
                };
                reader.readAsDataURL(file);
            };
            input.click();
        });
    });


















function showCalc() {
  document.getElementById("arbCalc").style.display = "block"
  document.getElementById("arbCalc").style.opacity = "1"
}

function hideCalc() {
  document.getElementById("arbCalc").style.display = "none"
  document.getElementById("arbCalc").style.opacity = "0"
}



function openModal() {
  // document.getElementById('deleteModal').style.display = 'block';
  document.getElementById('modalBox').style.opacity = '1';
  document.getElementById('modalBox').style.display = 'block';
  // document.getElementById('modalContent').style.marginTop = '20%'
  document.body.style.overflow = 'hidden'; // Prevent scrolling behind the modal
  console.log('works')
}

function closeModal() {
  document.getElementById('modalBox').style.display = 'none';
  document.body.style.overflow = 'auto'; // Allow scrolling again
}

function deleteEvent() {
  // Add logic here to handle the deletion of the event
  document.getElementById("arbBox").style.display = "none"
  closeModal();
}


// To cpoy match text

const club1 = document.querySelector('.club1');
const club2 = document.querySelector('.club2');



function copyMatchText() {
  copyText('match-text');
}

function copyClub1Text() {
  copyText('club1'); // Correct argument passed
}

function copyClub2Text() {
  copyText('club2'); // Correct argument passed
}

function copyText(elementClass) {
  var textToCopy = document.getElementById(elementClass).innerText;
  // ... rest of the code remains the same ...
  var tempTextArea = document.createElement('textarea');
  tempTextArea.value = textToCopy;
  document.body.appendChild(tempTextArea);
  tempTextArea.select();
  tempTextArea.setSelectionRange(0, 99999);
  document.execCommand('copy');
  document.body.removeChild(tempTextArea);
  alert('Text copied to clipboard: ' + textToCopy);
}



// create bookmakers 


// create bookmakers 
console.log("Script is running");
const bookmakers = [
  "10Bet",
  "10Bet (UK)",
  //"10Cric",
  //"12Bet",
  //"12Bet (BTI)",
  //"188Bet",
  //"18Bet",
  //"1Bet",
  //"1Win",
  "1xBet",
  "1xBet (IT)",
  "1xBet (NG)",
  "22Bet",
  "3et",
  "888sport",
  "888sport (IT)",
  "AccessBET",
  //"AdjaraBet",
  //"AdmiraLbet (IT)",
  //"AmuletoBet",
  "AsianOdds",
  //"Bahigo",
  //"BaltBet",
  //"Bangbet",
  //"Bantubet",
  //"Bet-at-home",
  //"Bet-Bra",
  //"Bet3000",
  "Bet365",
  "Bet7",
  "Bet9ja",
  "BetaBet",
  "Betaland (IT)",
  "Betano",
  "Betano (BR)",
  "Betano (NG)",
  "Betanoshops (Betbiga)",
  "Betbonanza",
  //"Betboo",
  "BetBoom",
  "Betboro",
  "Betboro (GH)",
  //"Betcenter (BE)",
  //"BetCity",
  //"Betcity (BY)",
  //"Betcity (NET)",
  //"Betcity (NL)",
  //"Betcity (RU)",
  //"BetClic",
  //"BetClic (FR)",
  //"BetClic (IT)",
  //"BetClic (PL)",
  //"BetClic (PT)",
  //"Betcoin",
  //"Betcris",
  //"Betcris (BR)",
  //"Betcris (DO)",
  //"Betcris (MX)",
  "BetDaq",
  "BetFair",
  //"Betfair (AU)",
  //"Betfair (ES)",
  //"Betfair (IT)",
  //"BetFair (MBR)",
  //"Betfair (RO)",
  //"Betfair (SE)",
  //"Betfair SB",
  //"Betfair SB (ES)",
  //"Betfair SB (RO)",
  //"Betfarm",
  //"Betfast (IO)",
  //"Betfinal",
  //"Betfirst (BE)",
  //"Betflag",
  //"Betflip (SPORT)",
  //"Betfred",
  //"BetFury",
  //"Bethard",
  "Betibet",
  "Betika (KE)",
  "BetInAsia (BLACK)",
  "BetKing",
  //"Betmais",
  //"Betmaster",
  "Betmgm (NY)",
  //"Betmotion",
  //"Betnacional",
  "BetObet",
  "BetOnline",
  //"BetOnline (classic)",
  //"Betonngliga",
  "Betonred (NG)",
  //"BetPawa (CM)",
  "BetPawa (GH)",
  "BetPawa (KE)",
  "BetPawa (NG)",
  "BetPawa (RW)",
  "BetPawa (TZ)",
  "BetPawa (UG)",
  "BetPawa (ZM)",
  //"BetPix365",
  //"BetPlay",
  //"BetRebels",
  //"Bets10",
  "Betsafe",
  //"Betsafe (LT)",
  "Betshop",
  "Betsson",
  //"Betsson (CO)",
  //"Betsson (ES)",
  //"Betsson (GR)",
  //"Betsul",
  //"Bettery (RU)",
  //"BetTilt",
  "BetVictor",
  //"Betvictor (ZH)",
  //"BetVision",
  //"BetWarrior",
  //"BetWarrior (PT)",
  "BetWay",
  //"BetWay (IT)",
  //"BetWay (PT)",
  "Betwgb",
  //"BetWill (IT)",
  "Betwinner",
  //"BetX (IT)",
  //"BFB247",
  //"Bildbet",
  //"Bingoal",
  //"Bingoal (NL)",
  //"Blaze",
  //"BloodMoon",
  //"BlueChip",
  "Bodog (EN)",
  //"Bodog (ES)",
  //"Bodog (EU)",
  //"Bodog (PT)",
  //"BolsaDeAposta",
  //"Bolsadeaposta SB",
  //"BookMaker",
  //"Boom Casino",
  "Bovada",
  "BoyleSports",
  //"BTC365 (Esports)",
  //"BuddyBet",
  //"Bumbet",
  "Bwin",
  //"Bwin (BE)",
  //"Bwin (DE)",
  //"Bwin (ES)",
  //"Bwin (FR)",
  //"Bwin (GR)",
  //"Bwin (IT)",
  //"Bwin (PT)",
  //"Caliente",
  "Campeonbet",
  //"CampoBet",
  //"Cannonbet",
  //"CasaDeApostas (PT)",
  //"Casapariurilor (RO)",
  //"Cashpoint",
  //"Cashpoint (DK)",
  //"Casino Spinamba",
  //"CasinoBarcelona (ES)",
  //"Casinostugan",
  //"Casinozer",
  //"Casobet (SPORT)",
  //"Casumo",
  //"Casumo (ES)",
  //"CBet (LT)",
  //"Chance (CZ)",
  //"Circus (BE)",
  //"Circus (NL)",
  "CloudBet",
  //"CMD368",
  "Codere (ES)",
  //"Codere (MX)",
  //"Comeon",
  "CoolBet",
  "Coral",
  //"Crystalbet",
  "Dafabet (Dafa Sports)",
  "Dafabet (OW)",
  //"Danskespil (DK)",
  //"Daznbet (ES)",
  //"DaznBet (UK)",
  //"DBbet",
  //"DomusBet (IT)",
  //"DoradoBet",
  "Draftkings",
  //"Drinbetzero",
  //"Ebingo",
  //"Ecuabet",
  //"EDSBet",
  //"Efbet (BG)",
  //"EfBet (ES)",
  //"EfBet (Net)",
  //"Efbet (RO)",
  //"Efbet (RS)",
  //"Esporte365",
  //"Esportenet (BET)",
  //"EsportesDaSorte (COM)",
  //"EstorilSolCasinos (PT)",
  //"Estrelabet",
  //"Etopaz (AZ)",
  //"EuroBet",
  //"EuropeBet",
  //"EveryGame (Intertops)",
  //"Exclusivebet",
  //"Expekt",
  //"Explosino",
  //"F12Bet",
  //"Fairspin (SPORT)",
  "FanDuel",
  //"FastBet",
//"FastBet (IT)",
//"FavBet",
//"FezBet",
//"Firebet (PT)",
//"FonBet",
//"Fonbet (GR)",
//"Fonbet (KZ)",
//"Fonbet (Mobile)",
//"Fortuna (CZ)",
//"Fortuna (PL)",
//"Fortuna (RO)",
//"Fortuna (SK)",
//"Fortune Clock",
//"Fortunejack",
//"Freeggbet",
//"Freshbet",
//"Fulltbet",
//"Fun88 (SPORT)",
//"GaleraBet",
//"Gamdom (SPORT)",
//"Game-365 (cn)",
//"Gamebookers",
//"Germania (HR)",
"GGBet",
"GGBet (com)",
//"Giocodigitale (IT)",
//"GoldBet",
//"GoldbetShop",
//"Golden Palace",
//"Goldenbet",
//"GoldenPark",
//"Gra (LIVE)",
//"GrandGame (gg.by)",
//"Greatwin",
//"GrosvenorCasinos",
//"Guts",
//"Hajper",
//"Hash636 (COM)",
//"HGA030",
//"HGA035",
//"Holiganbet",
//"Holland Casino",
//"IForBet",
//"Inkabet",
//"Interwetten",
//"Interwetten (ES)",
//"Interwetten (GR)",
//"IntralotShop",
//"IviBet",
//"IviBet (GR)",
//"IviCasino",
//"JackBet",
//"Jackbit",
//"Jacks",
//"Jokerbet",
//"Joycasino",
//"Juegging (ES)",
//"Justbet",
//"Kakeyo",
//"KirolBet",
//"KTO",
"Ladbrokes",
//"Ladbrokes (DE)",
//"Leon",
//"LeoVegas",
//"LeoVegas (ES)",
//"LeoVegas (IT)",
//"LeoVegas (PT)",
//"Levebet",
//"Librabet",
//"LigaStavok",
//"Linebet",
"Livescorebet (IE)",
"Livescorebet (NG)",
"Livescorebet (NL)",
"Livescorebet (UK)",
//"Lootbet (SPORT)",
//"Lottomatica",
//"LsBet",
//"Luckia",
//"Lucky Bird Casino",
//"Lucky Block",
//"Lvbet",
//"Lvbet (LV)",
//"Lvbet (PL)",
//"Lyllo Casino",
//"M88",
//"Magic Win",
//"Mansion (M88-BTI)",
//"Mansion88",
"Marathonbet",
//"Marathon (BY)",
//"Marathon (DK)",
//"Marathon (ES)",
//"Marathon (RU)",
"Marathonbet (IT)",
//"Marca Apuestas",
//"Marjosports",
//"MarsBet",
//"Matchbook",
//"MaxLine",
"MBet",
"MegaPari",
"MelBet",
//"MelBet (NG)",
//"MelBet (RU)",
"MerryBet",
//"MobileBet",
//"MostBet",
"Mozzart",
//"Mozzart (GH)",
//"Mozzart (NG)",
//"Mozzart (RO)",
//"MrGreen",
//"MrJack",
//"MrSloty",
//"MrXBet",
"Msport (GH)",
"Msport (NG)",
//"MyBet",
//"MyStake",
//"Mystake (BET)",
"N1bet",
"N1bet (NG)",
"NairaBet",
//"Neobet",
//"Neobet (DE)",
//"Nesine",
//"NetBet",
//"Netbet (BR)",
//"NetBet (GR)",
//"NetBet (IT)",
//"NetBet (RO)",
//"Nextbet",
//"NitroBetting",
//"Nopeampi",
//"NordicBet",
//"NoviBet (BR)",
//"Novibet (CO.UK)",
//"Novibet (GR)",
//"Novibet (IE)",
//"Oddset (DE)",
"Olimp",
//"Olimp",
"Olimpbet",
//"Olimpbet (KZ)",
//"Olimpobet",
//"OlyBet",
//"Olybet (ES)",
//"OrbiteX",
"OrbitX",
"Paddy Power",
//"Paf (COM)",
//"Paf (ES)",
//"Paf (SE)",
//"PafBet (LV)",
//"PameStoixima",
//"Parasino",
//"Pari",
"Parimatch (BR)",
"Parimatch (CO.UK)",
"Parimatch (CY)",
"Parimatch (KZ)",
"Parimatch (NG)",
"Paripesa (COM)",
"Paripesa (NG)",
//"Partypoker",
//"Paston (Altenar)",
//"Pin-up",
//"Pin-up (EN)",
//"Pin-up (RU)",
//"Pin135 (ASIAN)",
"Pinnacle",
"Pinnacle (BET)",
"Pinnacle (IT)",
"Pinnacle (SE)",
"Pinnacle888 (ASIAN)",
//"PIWI247",
//"PixBet",
//"Placard (PT)",
//"PlanetWin365 (IT)",
//"Playbound",
//"Playpix",
//"Plexbet (IT)",
//"PokerStars",
//"PokerStars (ES)",
//"PokerStars (FR)",
//"PokerStars (IT)",
//"PokerStars (SE)",
//"PowBet",
//"Premium Tradings",
"PS3838",
//"Psk (HR)",
//"Punt",
//"Pzbuk",
//"Rabona",
//"Redbet",
//"ReloadBet",
//"RETAbet (ES)",
//"RETAbet (ES-AN)",
//"RingoBet (Fairplay)",
//"Rivalo",
//"Rivalo (CO)",
//"Rivalry",
//"Rollbit",
//"RooBet",
//"Rushbet",
//"Saga Kingdom",
//"Sapphirebet",
"SboBet",
"Sbobet (eSport IM)",
"Sbobet(pic5678.com)",
"SbobetAsia",
//"SboTop",
//"Sinobet10",
//"Sisal",
//"SkyBet",
//"Slots Safari",
//"Slottica",
//"Slotty Way",
//"Smarkets",
//"Snabbare",
//"Snai",
//"Solcasino",
//"Solverde",
//"Sportaza",
//"Sportbet (IT)",
//"SportBet24",
"Sportingbet",
"Sportingbet (DE)",
"Sportingbet (GR)",
"Sportingbet (PT-BR)",
"Sportingbet (RO)",
"Sportingbet (ZA)",
//"SportingWin",
//"Sportium (CO)",
//"Sportium (ES)",
"Sportmarket",
"SportsBet (BR)",
"SportsBet (IO)",
"Sportsbetio (UK)",
"sportsbetting.ag",
"SportyBet",
"Stake",
//"StarCasinoSport",
//"StarGame (IT)",
//"Stoiximan",
//"Stoiximan EN",
//"STS",
//"SuperBet new",
//"SuperBet (PL) new",
//"SuperBet (RO) new",
//"SuperBet88 new",
"Suprabets",
"Surebet247",
//"Svenska Spel",
"TempoBet",
"Tennisi",
"Tennisi (bet)",
"Tennisi (KZ)",
//"TigerGaming",
//"Tipbet",
//"Tipico",
//"Tipico (DE)",
//"Tippmixpro",
//"Tipsport (CZ)",
//"Tipsport (SK)",
//"TitanBet",
//"TonyBet",
//"Tonybet (ES) (Circus)",
//"Tonybet (UK)",
//"TornadoBet",
//"Toto",
//"TOTOgaming",
//"Totogaming (RU)",
//"Tradexbr",
//"TrBET",
//"Uabet",
//"UBC365",
//"Ubet",
//"UniBet",
//"Unibet (AU)",
//"Unibet (CO.UK)",
//"Unibet (FR)",
//"Unibet (GR)",
//"Unibet (IT)",
//"Unibet (NL)",
//"Unibet (RO)",
//"Vaidebet",
//"Vave",
"VBet",
"VBet (AM)",
"VBet (CO.UK)",
"Vbet (LAT)",
"Vbet (NL)",
//"Vegas (HU)",
//"Veikkaus",
//"Versus (ES)",
//"Vistabet (GR)",
//"VKGame (CC)",
//"Vulkan",
//"Vulkan Bet",
//"W88Live",
"Wazobet",
//"Weiss (SPORT)",
"William Hill",
"Williamhill (ES)",
"Williamhill (IT)",
"Williamhill (SE)",
//"Winamax",
//"Winamax (DE)",
//"Winamax (ES)",
//"Winamax (FR)",
//"Winbet (BG)",
//"Winbet (RO)",
//"Winline (RU)",
//"WinlineBet.com",
//"Winmasters",
//"Winmasters (CY)",
//"Winmasters (GR)",
//"Winmasters (RO)",
//"Wplay (CO)",
//"WWin",
//"XTiP (DE)",
//"Yaasscasino",
//"Yajuego (CO)",
//"Yonibet",
//"YSB",
//"Zamba (ES)",
"ZEbet",
"ZEbet (BE)",
"ZEbet (ES)",
"ZEbet (FR)",
"ZEbet (NG)",
"ZEbet (NL)",
//"Zenit",
//"Zenit (WIN)",
//"ZigZag 777",
//"ZigZag Sport",
//"Zulabet"
];
// Function to generate checkboxes dynamically
// Function to generate checkboxes dynamically
function generateCheckboxes() {
  const bookmakersList = document.getElementById("bookmakersList");
  
  bookmakers.forEach(bookmaker => {
      const div = document.createElement("div");
      div.classList.add("bookmaker-item");
  
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.id = bookmaker;
  
      const label = document.createElement("label");
      label.htmlFor = bookmaker;
      label.textContent = bookmaker;
  
      div.appendChild(checkbox);
      div.appendChild(label);
  
      bookmakersList.appendChild(div);
  });
  }

// Call the function to generate checkboxes
generateCheckboxes();


  let bookiesBtn = document.getElementById('bookiesBtn');
  let sportsBtn = document.getElementById('sportssBtn');
  let bookmakersBox = document.getElementById('bookmakersBox');
  
  
  function showBookies() {
    bookmakersBox.style.display = 'block'
  }

  function closeBookMakersBox() {
    var bookmakersBox = document.getElementById("bookmakersBox");
    bookmakersBox.style.display = 'none';
    
}









const sportsArray = [
  "Air hockey",
  //"Air hockey 2x2",
  "American football",
  //"Australian football",
  //"Badminton",
  //"Bandy",
  "Baseball",
  "Basketball",
  "Basketball 3x3",
  //"Basketball 4x4",
  //"Beach football",
  //"Beach handball",
  //"Beach volleyball",
  //"Bowls",
  //"Chess",
  //"Cricket",
  //"Curling",
  "Darts",
  //"Esport",
  //"Arena of Valor",
  //"Call of Duty",
  //"Counter-Strike",
  //"Dota",
  "E-Basketball",
  "E-Football",
  "E-Hockey",
  "E-Tennis",
  "E-Volleyball",
  //"King of Glory",
  //"League of Legends",
  //"NBA2K",
  //"Overwatch",
  //"Rainbow",
  //"Rocket League",
  //"StarCraft",
  //"Valorant",
  //"Warcraft",
  "Field hockey",
  "Floorball",
  "Football",
  "Football 3x3",
  //"Football 4x4",
  //"Football 5x5",
  "Futsal",
  //"Gaelic football",
  "Golf",
  "Handball",
  "Hockey",
  //"Hurling",
  //"Lacrosse",
  "Martial arts",
  //"Netball",
  //"Pesäpallo",
  "Rugby",
  //"Short Hockey",
  "Snooker",
  "Table tennis",
  "Tennis",
  //"Virtual sports",
  //"Basketball (SRL)",
  //"Cricket (SRL)",
  //"Football (SRL)",
  //"Tennis (SRL)",
  //"Volleyball",
  //"Water polo",
  //"What Where When"
];

function generateSportsCheckboxes() {
  const sportsList = document.getElementById("sportsList");

  let currentRow = null;

  sportsArray.forEach(sport => {
      // Check if the current row needs to be created
      if (!currentRow) {
          currentRow = document.createElement("div");
          currentRow.classList.add("checkbox-row");
          sportsList.appendChild(currentRow);
      }

      const div = document.createElement("div");
      div.classList.add("sport-item");

      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.id = sport;

      const label = document.createElement("label");
      label.htmlFor = sport;
      label.textContent = sport;

      div.appendChild(checkbox);
      div.appendChild(label);

      currentRow.appendChild(div);

      // Check if the current row is full (adjust this value based on your layout)
      if (currentRow.children.length >= 10) {
          currentRow = null; // Start a new row
      }
  });
}

// Call the function to generate sports checkboxes
generateSportsCheckboxes();



let sportsBox = document.getElementById('sportsBox');


function showSports() {
  sportsBox.style.display = 'block'
}

function closeSportsBox() {
  var sportsBox = document.getElementById("sportsBox");
  sportsBox.style.display = 'none';
  
}

document.addEventListener('DOMContentLoaded', () => {
      const surebetMap = new Map();
      
      function roundProfit(profit) {
        return Math.round(profit * 100) / 100;
      }
      
      function timeSince(pastTimeStr) {
        const referenceTime = new Date(); // Get the current time
        const pastTime = new Date(pastTimeStr); // Convert the past time string to a Date object
        
        const timeDiff = referenceTime - pastTime; // Calculate the difference in milliseconds
      
        // Determine the appropriate unit (seconds, minutes, hours, or days)
        const secondsInDay = 86400000;
        const minutesInHour = 60;
      
        if (timeDiff >= secondsInDay) {
          return Math.floor(timeDiff / secondsInDay) + 'd ago';
        } else if (timeDiff >= minutesInHour * 60 * 1000) { // Check for hours (at least 1 minute)
          return Math.floor(timeDiff / (minutesInHour * 60 * 1000)) + 'h ago';
        } else if (timeDiff >= minutesInHour * 1000) { // Check for minutes (at least 1 second)
          return Math.floor(timeDiff / (minutesInHour * 1000)) + 'm ago';
        } else {
          // Less than a minute, ensure output between 0-59 seconds
          return Math.min(Math.floor(timeDiff / 1000), 59) + 's ago'; // Limit to 59 seconds
        }
      }

      let fetchIntervalId;

      async function fetchSurebets() {
        try {
          const cachedData = JSON.parse(localStorage.getItem('surebets'));

          if (cachedData) {
            console.log('Using cached Data');
            await populateSurebets(cachedData);
          }

          const response = await fetch('http://172.20.10.5:5000/api/v1/surebets'); // Replace with your actual endpoint URL
          const data = await response.json();

          if (data) {
            console.log("Using Api Data")
            console.log(data)
            await populateSurebets(data); // Call function to populate HTML
            // Store the fetched data in localStorage or sessionStorage
            localStorage.setItem('surebets', JSON.stringify(data));
            sessionStorage.setItem('surebets', JSON.stringify(data));
          } else {
            console.error('No surebets found');
          }
        }
        catch (error) {
          console.error('Error fetching surebets:', error);
        }
        finally {
          fetchIntervalId = setTimeout(fetchSurebets, 30); 
        //setTimeout(fetchSurebets, 30); // Fetch again every 3 seconds
        }
      }

      fetchSurebets();


      // Function to check if a surebet needs updating
      function hasSurebetChanged(newData, oldElement) {
        // Check basic data (id, gametime, bookmakers)
        if (newData.id !== oldElement.getAttribute('surebetId') ||
            newData.gametime !== oldElement.querySelector('#Event-time').textContent ||
            newData.bookmaker1 !== oldElement.querySelector('#bookie-name1').textContent ||
            newData.bookmaker2 !== oldElement.querySelector('#bookie-name2').textContent ||
            newData.bookmaker3 !== oldElement.querySelector('#bookie-name3').textContent) {
          return true;
        }
        
        // Checking for profit changes
        const oldProfit = parseFloat(oldElement.querySelector('.percentage').textContent.split('%')[0]);
        if (roundProfit(newData.profit) !== oldProfit) {
          return true;
        }

        // Checking for odds changes
        const oldOdds1 = parseFloat(oldElement.querySelector('#odds1').textContent);
        const newOdds1 = newData.market_1_odds;
        if (Math.abs(oldOdds1 - newOdds1) > 0.01) { // Adjust threshold for significant change
          return true;
        }
      
        const oldOdds2 = parseFloat(oldElement.querySelector('#odds2').textContent);
        const newOdds2 = newData.market_2_odds;
        if (Math.abs(oldOdds2 - newOdds2) > 0.01) {
          return true;
        }
      
        const oldOdds3 = parseFloat(oldElement.querySelector('#odds3').textContent);
        const newOdds3 = newData.market_3_odds;
        if (Math.abs(oldOdds3 - newOdds3) > 0.01) {
          return true;
        }
      
        // ... other checks if needed
        return false;        
      }


      // Function to Update a surebet element in the Dom
      function updateSurebetElement(element, data) {
        console.log("I'm in the UpdateSurebetElement Function")
        const percentElement = element.querySelector('.percentage');
        const percentageValue = roundProfit(data[i].profit);
        found_at = data[i].found_at
        percentElement.innerHTML = `${percentageValue}%<br><span class="time" id="time-ago">${timeSince(found_at)}</span`;

        const eventNameElement = element.querySelector('#event-name');
        eventNameElement.innerHTML = `${data[i].sport_type}<br><span class="event-time" id="Event-time">${data[i].gametime}</span>`;
        //console.log("event ELEMENT SET")

      
        const marketElement = element.querySelector('#arb-market');
        marketElement.textContent = data[i].market1type;
        //console.log("market ELEMENT SET")
        
        const bookmaker1Element = element.querySelector('#bookie-name1');
        bookmaker1Element.textContent = data[i].bookmaker1;
        
        //console.log("bookmaker1 set")
        const club1Element = element.querySelector('#club1');
        teams = JSON.parse(data[i].teams)
        club1Element.textContent = teams[0];
        //console.log("club1 is ", teams[0])

        //console.log("club1 set")
        const club2Element = element.querySelector('#club2');
        club2Element.textContent = teams[1];
        //console.log("club2 is ", teams[1])

        //console.log("club2 set")
        const CL1_Element = element.querySelector('#country_league1');
        CL1_Element.textContent = data[i].tournament;

        //console.log("Country_league set")
        const market1Element = element.querySelector('#market1');
        const marketInfo = data[i].market1 + ' ' + data[i].market_1_condition;
        market1Element.textContent = marketInfo;

        //console.log("market 1 set")
        const odds1Element = element.querySelector('#odds1');
        odds1Element.textContent = data[i].market_1_odds;


        const bookmaker2Element = element.querySelector('#bookie-name2');
        bookmaker2Element.textContent = data[i].bookmaker2;
        
        //console.log("bookmaker2 set")
        const club21Element = element.querySelector('#club21');
        club21Element.textContent = teams[0];

        const club22Element = element.querySelector('#club22');
        club22Element.textContent = teams[1];

        const CL2_Element = element.querySelector('#country_league2');
        CL2_Element.textContent = data[i].tournament;

        //console.log("Country_league set")
        const market2Element = element.querySelector('#market2');
        const market2Info = data[i].market2 + ' ' + data[i].market_2_condition;
        market2Element.textContent = market2Info;

        //console.log("market 1 set")
        const odds2Element = element.querySelector('#odds2');
        odds2Element.textContent = data[i].market_2_odds;



        const bookmaker3Element = element.querySelector('#bookie-name3');
        bookmaker3Element.textContent = data[i].bookmaker3;
        
        //console.log("bookmaker3 set")
        const club31Element = element.querySelector('#club31');
        club31Element.textContent = teams[0];

        const club32Element = element.querySelector('#club32');
        club32Element.textContent = teams[1];

        const CL3_Element = element.querySelector('#country_league3');
        CL3_Element.textContent = data[i].tournament;

        //console.log("Country_league set")
        const market3Element = element.querySelector('#market3');
        const market3Info = data[i].market3 + ' ' + data[i].market_3_condition;
        market3Element.textContent = market3Info;

        //console.log("market 1 set")
        const odds3Element = element.querySelector('#odds3');
        odds3Element.textContent = data[i].market_3_odds;

        const matchLinks = JSON.parse(data[i].match_nav_list);
        
        const marketLinks = JSON.parse(data[i].market_nav_list);

        let teamLinks;
        if (matchLinks.length === 3) {
          teamLinks = matchLinks;
        } else {
          teamLinks = marketLinks;
        }
        //console.log("team links are ", teamLinks)

        const matchTextElement = element.querySelectorAll('#match-text');
        for (let j = 0; j < matchTextElement.length; j++) {
          const teamSpan = matchTextElement[j];
          const teamLink = teamLinks[j];
      
          if (teamLink) {
            const teamLinkElement = document.createElement('a');
            teamLinkElement.href = teamLink;
            teamLinkElement.textContent = teamSpan.textContent;
            teamLinkElement.target = "_blank";
            teamLinkElement.style.textDecoration = "none";
            teamSpan.parentNode.replaceChild(teamLinkElement, teamSpan);
          }
        }
        //// Update percentage, odds, etc. based on your logic
        //element.querySelector('.percentage').textContent = `${Math.ceil(newData.profit * 10) / 10}%<br><span class="time" id="time-ago">${timeSince(newData.found_at)}</span`;
        //element.querySelector('#Event-time').textContent = newData.gametime;
        // ... update other elements
      
        //// Highlight odds change (optional)
        //const oddsElements = element.querySelectorAll('.odds');
        //for (const oddsElement of oddsElements) {
        //  const oldOdds = parseFloat(oddsElement.textContent);
        //  const newOdds = parseFloat(newData[oddsElement.id.substring(4)]); // Assuming id format like "odds1"
        //  if (Math.abs(oldOdds - newOdds) > 0.01) {
        //    oddsElement.classList.add('odds-changed'); // Add a CSS class for styling
        //  }
        //}
      }

      function roundProfit(profit) {
        return Math.round(profit * 100) / 100;
      }

      // This Function removes old Surebet
      function removeOldSurebets(surebetMap, data) {
          // Loop through existing surebets and check for removal
          for (const [surebetId, element] of surebetMap.entries()) {
            if (!data.some(newData => newData.id === surebetId)) {
              element.parentNode.removeChild(element);
              surebetMap.delete(surebetId); // Remove from map as well
            }
          }
      }

      // Function to Populate Surebets
      async function populateSurebets(data) {
        const arbSec = document.querySelector('.arb-sec');
        const allArbs = arbSec.querySelector('#allArbs')
        const originalArbBox = allArbs.querySelector('#arbBox');
        originalArbBox.style.display = 'none'
        //const tempBox = originalArbBox.cloneNode(true);
        removeOldSurebets(surebetMap, data)

        for (let i = 0; i < data.length; i++) {
          const newArbBox = originalArbBox.cloneNode(true); // Clone with content
          //originalArbBox.parentNode.removeChild(originalArbBox);
          const existingElement = surebetMap.get(data[i].id)
          //originalArbBox.innerHTML = '';

          // Check if element exists
          if (existingElement) {
            // Existing surebet - Update if data has changed
            if (hasSurebetChanged(data[i], existingElement)) {
              updateSurebetElement(existingElement, data[i]);
            }
            surebetMap.set(data[i].id, existingElement);
          } else {
              newArbBox.setAttribute('surebetId', data[i].id);
              
              const percentElement = newArbBox.querySelector('.percentage');
              const percentageValue = roundProfit(data[i].profit);
              found_at = data[i].found_at
              percentElement.innerHTML = `${percentageValue}%<br><span class="time" id="time-ago">${timeSince(found_at)}</span`;

              const eventNameElement = newArbBox.querySelector('#event-name');
              eventNameElement.innerHTML = `${data[i].sport_type}<br><span class="event-time" id="Event-time">${data[i].gametime}</span>`;
              //console.log("event ELEMENT SET")

            
              const marketElement = newArbBox.querySelector('#arb-market');
              marketElement.textContent = data[i].market1type;
              //console.log("market ELEMENT SET")
              
              const bookmaker1Element = newArbBox.querySelector('#bookie-name1');
              bookmaker1Element.textContent = data[i].bookmaker1;
              
              //console.log("bookmaker1 set")
              const club1Element = newArbBox.querySelector('#club1');
              teams = JSON.parse(data[i].teams)
              club1Element.textContent = teams[0];
              //console.log("club1 is ", teams[0])

              //console.log("club1 set")
              const club2Element = newArbBox.querySelector('#club2');
              club2Element.textContent = teams[1];
              //console.log("club2 is ", teams[1])

              //console.log("club2 set")
              const CL1_Element = newArbBox.querySelector('#country_league1');
              CL1_Element.textContent = data[i].tournament;

              //console.log("Country_league set")
              const market1Element = newArbBox.querySelector('#market1');
              const marketInfo = data[i].market1 + ' ' + data[i].market_1_condition;
              market1Element.textContent = marketInfo;

              //console.log("market 1 set")
              const odds1Element = newArbBox.querySelector('#odds1');
              odds1Element.textContent = data[i].market_1_odds;


              const bookmaker2Element = newArbBox.querySelector('#bookie-name2');
              bookmaker2Element.textContent = data[i].bookmaker2;
              
              //console.log("bookmaker2 set")
              const club21Element = newArbBox.querySelector('#club21');
              club21Element.textContent = teams[0];

              const club22Element = newArbBox.querySelector('#club22');
              club22Element.textContent = teams[1];

              const CL2_Element = newArbBox.querySelector('#country_league2');
              CL2_Element.textContent = data[i].tournament;

              //console.log("Country_league set")
              const market2Element = newArbBox.querySelector('#market2');
              const market2Info = data[i].market2 + ' ' + data[i].market_2_condition;
              market2Element.textContent = market2Info;

              //console.log("market 1 set")
              const odds2Element = newArbBox.querySelector('#odds2');
              odds2Element.textContent = data[i].market_2_odds;



              const bookmaker3Element = newArbBox.querySelector('#bookie-name3');
              bookmaker3Element.textContent = data[i].bookmaker3;
              
              //console.log("bookmaker3 set")
              const club31Element = newArbBox.querySelector('#club31');
              club31Element.textContent = teams[0];

              const club32Element = newArbBox.querySelector('#club32');
              club32Element.textContent = teams[1];

              const CL3_Element = newArbBox.querySelector('#country_league3');
              CL3_Element.textContent = data[i].tournament;

              //console.log("Country_league set")
              const market3Element = newArbBox.querySelector('#market3');
              const market3Info = data[i].market3 + ' ' + data[i].market_3_condition;
              market3Element.textContent = market3Info;

              //console.log("market 1 set")
              const odds3Element = newArbBox.querySelector('#odds3');
              odds3Element.textContent = data[i].market_3_odds;

              const matchLinks = JSON.parse(data[i].match_nav_list);
              
              const marketLinks = JSON.parse(data[i].market_nav_list);

              let teamLinks;
              if (matchLinks.length === 3) {
                teamLinks = matchLinks;
              } else {
                teamLinks = marketLinks;
              }
              //console.log("team links are ", teamLinks)

              const matchTextElement = newArbBox.querySelectorAll('#match-text');
              for (let j = 0; j < matchTextElement.length; j++) {
                const teamSpan = matchTextElement[j];
                const teamLink = teamLinks[j];
            
                if (teamLink) {
                  const teamLinkElement = document.createElement('a');
                  teamLinkElement.href = teamLink;
                  teamLinkElement.textContent = teamSpan.textContent;
                  teamLinkElement.target = "_blank";
                  teamLinkElement.style.textDecoration = "none";
                  teamSpan.parentNode.replaceChild(teamLinkElement, teamSpan);
                }
              }
            

              surebetMap.set(data[i].id, newArbBox);
              newArbBox.style.display = 'block'
              arbSec.appendChild(newArbBox);
            }
      }
    }

      // Call the function to duplicate the arb-box
      populateSurebets();
      
      // Restart the fetch request when the user returns to the Arb page
      function startFetchInterval() {
        if (!fetchIntervalId) {
          fetchSurebets();
        }
      }

      // Clear the fetch interval when the user leaves the Arb page
      function stopFetchInterval() {
        if (fetchIntervalId) {
          clearTimeout(fetchIntervalId);
          fetchIntervalId = null;
        }
      }
      // Call startFetchInterval when the Arb page is loaded
      startFetchInterval();

      // Call stopFetchInterval when the user navigates away from the Arb page
      window.addEventListener('beforeunload', stopFetchInterval);

    });

function aside(){
  const sidebar = document.querySelector(".fixed-side");
  const main = document.querySelector(".main");
  sidebar.classList.toggle("active");
  main.classList.toggle("active");
}