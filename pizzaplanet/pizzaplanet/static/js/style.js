/*

getElementById() for DOM ids
querySelector() for DOM classes

or, if you want to be particularly annoying,

getElementsByClassName()

*/

const pizzaSpain = document.getElementById("pizza");
const tScale = document.getElementById(".tOut")
let rotation = 0;
let scale = 1;
let index = 0;
let flag = 0;


window.onload=function() {
  slide(index + 1);
}

function  startRotation() {
let rFlag = 0;

setInterval(() => {
  rotation += 360; 
  scale = scale === 1 ? 0.5 : 0.8;
  pizzaSpain.style.transform = `rotate(${rotation}deg)  scale(${scale})`; 
}, 500);}


// function startScale(anchor) {
//   scale = scale === 1 ? 1 : 4;
//   anchor.style.transform = `scale(${scale})`;
// }

function startScale(anchor) {
  nScale = nScale === 1 ? 1.5 : 1;
  anchor.style.transform = `scale(${nScale})`; 
  anchor.style.transition = "transform 0.2s ease"; 
}


function openNav() {
  if (flag == 0) {
    document.getElementById("mySidebar").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
    flag = 1;
  } else {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
    flag = 0;
  }
  }
  
  function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
    flag = 0;
  }

  function closeNavB() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
  }

  function preview() {
    const profPic = document.getElementById('file').files[0];
    const pView = new FileReader();

    pView.onloadend = function() {
      const preview = document.getElementById('new_pic');
      preview.src = pView.result;
      preview.style.display = "block";

    }

    if (profPic) {
      pView.readAsDataURL(profPic);
    }
  }

  function slideshow(n) {
    nextSlide(index += n);
  }

  function slide(n) {
    nextSlide(index = n);
  }

  function nextSlide(n) {
    let i;
    let slices = document.querySelectorAll('.slice');
    let marks = document.querySelectorAll('.mark');

    if (n > slices.length) {
      index = 1;
    }

    if (n < 1) {
      index = slices.length;
    }

    for (i = 0; i < slices.length; i++) {
      slices[i].style.display = "none";
    }

    for (i = 0; i < marks.length; i++) {
      marks[i].className = marks[i].className.replace(" active", "");
    }

    slices[index - 1].style.display="block";
    marks[index - 1].className += " active";

  }

//   function clicky() {
//     let oneTime = document.getElementById("generate").getAttribute("data-url");
//     console.log("Redirecting to:", oneTime);  
//     window.location.href = oneTime; 
// };
   


  //Terrible