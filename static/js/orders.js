document.addEventListener(
"DOMContentLoaded",
()=>{


const cards =
document.querySelectorAll(
".order-card"
);



cards.forEach(
(card,index)=>{


card.style.animationDelay =
`${index * 0.1}s`;



});


});