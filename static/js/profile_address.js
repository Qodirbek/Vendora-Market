document.addEventListener(
"DOMContentLoaded",
()=>{


const form =
document.getElementById("addressForm");


if(form){


form.addEventListener(
"submit",
()=>{


const btn =
document.querySelector(
".save-address"
);


btn.innerHTML =
"⏳ Saqlanmoqda...";


btn.disabled=true;



});


}



});