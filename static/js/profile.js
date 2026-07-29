document.addEventListener(
"DOMContentLoaded",
function(){



// =====================================
// CARD ANIMATION
// =====================================


const cards =
document.querySelectorAll(
".stat-card"
);



cards.forEach(card=>{


card.addEventListener(
"mouseenter",
()=>{

card.style.transform=
"translateY(-8px)";


});



card.addEventListener(
"mouseleave",
()=>{

card.style.transform=
"translateY(0)";


});


});





// =====================================
// BUTTON RIPPLE EFFECT
// =====================================


const buttons =
document.querySelectorAll(
"a,button"
);



buttons.forEach(btn=>{


btn.addEventListener(
"click",
function(e){


let ripple =
document.createElement(
"span"
);


ripple.className=
"ripple";


this.appendChild(
ripple
);



setTimeout(()=>{

ripple.remove();

},500);



});



});







// =====================================
// NUMBER COUNTER
// =====================================


const numbers =
document.querySelectorAll(
".stat-card h2"
);



numbers.forEach(num=>{


let value =
parseInt(
num.innerText
);



if(
isNaN(value)
)
return;



let start=0;


let duration=800;


let step =
value /
(duration/20);



let timer =
setInterval(()=>{


start += step;



if(start>=value){

start=value;

clearInterval(timer);

}



num.innerText=
Math.floor(start);


},20);



});






// =====================================
// ACTIVE MENU
// =====================================


let path =
window.location.pathname;



document
.querySelectorAll(
".menu-card a"
)
.forEach(link=>{


if(
link.getAttribute("href")
==
path
){


link.style.background=
"#eff6ff";


link.style.color=
"#2563eb";


}


});



});