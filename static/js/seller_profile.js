document.addEventListener(
"DOMContentLoaded",
()=>{


const edit =
document.getElementById(
"editProfile"
);


if(edit){

edit.onclick=function(){

alert(
"Profil tahrirlash oynasi tez orada qo'shiladi"
);

}

}



const buttons =
document.querySelectorAll(
".actions button"
);


buttons.forEach(btn=>{


btn.addEventListener(
"mouseenter",
()=>{

btn.style.transform="translateY(-3px)";

}
);



btn.addEventListener(
"mouseleave",
()=>{

btn.style.transform="translateY(0)";

}

);


});


});