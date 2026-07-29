document.addEventListener(
"DOMContentLoaded",
()=>{


const form=document.querySelector(
".status-card form"
);


if(form){

form.addEventListener(
"submit",
(e)=>{


let ok=confirm(
"Buyurtma statusini o'zgartirasizmi?"
);


if(!ok){

e.preventDefault();

}


});

}


});