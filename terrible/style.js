const pizzaSpain = document.getElementById("pizza"); // Use getElementById for ID selector
const tScale = document.getElementById(".tOut")


let rotation = 0;
let scale = 1;

function  startRotation() {
setInterval(() => {
  rotation += 360; // Increment rotation by 360 degrees each second
  scale = scale === 1 ? 0.5 : 0.8;
  pizzaSpain.style.transform = `rotate(${rotation}deg)  scale(${scale})`; // Apply rotation
}, 500);}


// function startScale(anchor) {
//   scale = scale === 1 ? 1 : 4;
//   anchor.style.transform = `scale(${scale})`;
// }

function startScale(anchor) {

  scale = scale === 1 ? 1.5 : 1;
  
  anchor.style.transform = `scale(${scale})`; 

  
  anchor.style.transition = "transform 0.3s ease"; // Smooth transition for the scale effect
}


function openNav() {
    document.getElementById("mySidebar").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
  }
  
  function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
  }

  //Terrible