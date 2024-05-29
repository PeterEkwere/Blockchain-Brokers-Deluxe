document.addEventListener("DOMContentLoaded", function () {
    var header = document.querySelector("header");
  
    window.addEventListener("scroll", function () {
      if (window.scrollY > 0) {
        header.style.boxShadow = "0px 4px 8px rgba(0, 0, 0, 0.1)";
      } else {
        header.style.boxShadow = "0px 3px 6px rgba(0, 0, 0, 0.1)";
      }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var sidepanel = document.getElementById('mySidepanel');
    var hamBtn = document.getElementById('toggleBtn');
    var hamDiv = document.getElementById('hamDiv');

    function closeSidePanel() {
        sidepanel.style.width = '0';
        hamDiv.classList.remove('closeNav');
        hamBtn.classList.remove('active');
    }

    hamBtn.addEventListener('click', function() {
        if (sidepanel.style.width === '170px') {
            closeSidePanel();
            
        } else {
            sidepanel.style.width = '170px';
            hamDiv.classList.add('closeNav');
            hamBtn.classList.add('active');
        }
    });



    // Close the side panel when clicking outside of it
    window.addEventListener('click', function(event) {
        if (event.target !== sidepanel && event.target !== hamBtn && sidepanel.style.width === '170px') {
            closeSidePanel();
        }
    });

    // Check window width and close side panel if width exceeds 1000px
    function checkWindowSize() {
        if (window.innerWidth > 1000 && sidepanel.style.width === '170px') {
            closeSidePanel();
        } else if (window.innerWidth <= 1000 && hamBtn.classList.contains('active')) {
            hamBtn.classList.remove('active');
        }
    }

    // Check window size initially and on resize
    window.addEventListener('resize', checkWindowSize);
    checkWindowSize();
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

    if (this.window.innerWidth < 1000){
      sidepanel.classList.remove("open");
      sidepanel.style.width = "0";
      openBtn.style.display = "inline";
      closeBtn.style.display = "none";
      freeBtn1.style.display = "none";
      document.getElementById("nav-links").style.display = "none"
    }
});


// var acc = document.getElementsByClassName("accordion");
// var i;

// for (i = 0; i < acc.length; i++) {
//   acc[i].addEventListener("click", function() {
//     this.classList.toggle("active");
//     var panel = this.nextElementSibling;
//     if (panel.style.maxHeight) {
//       panel.style.maxHeight = null;
//     } else {
//       panel.style.maxHeight = panel.scrollHeight + "px";
//     }
//   });
// }

var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function () {
        // Close all panels except the one being clicked
        var panels = document.querySelectorAll('.panel');
        panels.forEach(function(panel) {
            if (panel !== this.nextElementSibling) {
                panel.style.maxHeight = null;
            }
        }, this);

        // Reset rotation class for all icons
        var icons = document.querySelectorAll('.exp-icon');
        icons.forEach(function(icon) {
            icon.classList.remove('rotate');
        });

        // Toggle active class for the clicked accordion
        this.classList.toggle("active");
        var panel = this.nextElementSibling;
        if (panel.style.maxHeight) {
            panel.style.maxHeight = null;
        } else {
            panel.style.maxHeight = panel.scrollHeight + "px";
            // Toggle rotation class for the icon within the clicked accordion
            var icon = this.querySelector('.exp-icon');
            icon.classList.add('rotate');
        }
    });
}

window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  var btn = document.getElementById("back-to-top-btn");
  if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
    btn.style.display = "block";
  } else {
    btn.style.display = "none";
  }
}

function backToTop() {
  // Smooth scroll to top
  window.scrollTo({
    top: 0,
    behavior: "smooth"
  });
}









  