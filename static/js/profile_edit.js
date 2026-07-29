// ===============================
// PROFILE EDIT JS
// ===============================


document.addEventListener(
"DOMContentLoaded",
()=>{


const form =
document.getElementById(
"profileForm"
);



const button =
document.querySelector(
".save-btn"
);





// SAVE LOADING


if(form){


form.addEventListener(
"submit",
()=>{


if(button){


button.innerHTML =
"⏳ Saqlanmoqda...";


button.disabled=true;


}



});


}






// INPUT ANIMATION


const inputs =
document.querySelectorAll(
".input-box input"
);



inputs.forEach(input=>{


input.addEventListener(
"focus",
()=>{


input
.closest(".input-box")
.classList.add(
"active"
);


});





input.addEventListener(
"blur",
()=>{


input
.closest(".input-box")
.classList.remove(
"active"
);


});



});





});