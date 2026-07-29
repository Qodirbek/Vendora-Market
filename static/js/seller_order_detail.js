document.addEventListener(
"DOMContentLoaded",
()=>{


const buttons=document.querySelectorAll(
".btn"
);


buttons.forEach(btn=>{


btn.addEventListener(
"click",
function(){


this.style.opacity="0.6";

this.innerHTML="⏳ Yuklanmoqda...";


}

);



});



});