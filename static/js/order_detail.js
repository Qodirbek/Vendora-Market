document.addEventListener(
"DOMContentLoaded",
()=>{


const cards =
document.querySelectorAll(
".info-card,.products-card"
);


cards.forEach((card,index)=>{


card.style.animation=
`show .5s ease ${index*0.1}s`;


});



});