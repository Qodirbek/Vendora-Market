document.addEventListener(
"DOMContentLoaded",
()=>{


// bloklash tasdiqlash

let block=document.querySelector(".block");


if(block){

block.addEventListener(
"click",
(e)=>{

let ok=confirm(
"Bu sellerni bloklashni xohlaysizmi?"
);


if(!ok){

e.preventDefault();

}


});


}



// pul format

document
.querySelectorAll(".money-number")
.forEach(
(el)=>{

let num=
parseInt(el.innerText);


if(!isNaN(num)){

el.innerText=
num.toLocaleString()
+" so'm";

}


});


});