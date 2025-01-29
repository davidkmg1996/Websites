const pizzaSpain = document.getElementById("pizza");

/*
getElementById() for DOM ids
querySelector() for DOM classes

or, if you want to be particularly annoying,

getElementsByClassName method()


*/
const tScale = document.getElementById(".tOut")


let rotation = 0;
let scale = 1;
let flag = 0;

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
  scale = scale === 1 ? 1.5 : 1;
  anchor.style.transform = `scale(${scale})`; 
  anchor.style.transition = "transform 0.3s ease"; 
}


function openNav() {
  if (flag == 0) {
    document.getElementById("mySidebar").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
    flag = 1;
  } else {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
    flag = 0
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

  //Terrible