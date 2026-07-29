document.addEventListener(
"DOMContentLoaded",
()=>{


const form =
document.getElementById(
"categoryForm"
);



if(form){


form.addEventListener(
"submit",
()=>{


const btn =
document.querySelector(
".add-btn"
);


btn.innerHTML =
"⏳ Qo'shilmoqda...";


btn.disabled=true;


});


}



const inputs =
document.querySelectorAll(
"input"
);



inputs.forEach(
input=>{


input.addEventListener(
"focus",
()=>{

input.parentElement.classList.add(
"active"
);

});


input.addEventListener(
"blur",
()=>{

input.parentElement.classList.remove(
"active"
);

});


});


});

document.addEventListener(
"DOMContentLoaded",
()=>{


const buttons =
document.querySelectorAll(
".delete-category"
);


buttons.forEach(btn=>{


btn.addEventListener(
"click",
function(e){


let ok =
confirm(
"Kategoriyani o‘chirishni xohlaysizmi?"
);


if(!ok){

e.preventDefault();

}


});


});


});