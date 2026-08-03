// =====================================
// PASSWORD SHOW / HIDE
// =====================================


function togglePassword(id){


const password =
document.getElementById(id);



if(!password)
return;



if(password.type==="password"){


password.type="text";


}

else{


password.type="password";


}


}







// =====================================
// PHONE FORMAT
// +998 90 123 45 67
// =====================================


const phoneInput =
document.querySelector(
'input[name="phone"]'
);



if(phoneInput){



phoneInput.addEventListener(
"input",
function(){



let value =
this.value.replace(/\D/g,'');



if(value.startsWith("998")){


value=value.substring(3);


}



value=value.substring(0,9);



let result="";



if(value.length>0){

result=value.substring(0,2);

}



if(value.length>=3){

result+=" "
+
value.substring(2,5);

}



if(value.length>=6){

result+=" "
+
value.substring(5,7);

}



if(value.length>=8){

result+=" "
+
value.substring(7,9);

}



this.value=result;



});



}







// =====================================
// PASSWORD STRENGTH
// =====================================


const password =
document.getElementById(
"password"
);



if(password){



password.addEventListener(
"input",
function(){


let strength=0;



let value=this.value;



if(value.length>=6)

strength++;



if(/[A-Z]/.test(value))

strength++;



if(/[0-9]/.test(value))

strength++;



if(/[^A-Za-z0-9]/.test(value))

strength++;



let bar =
document.querySelector(
".password-strength div"
);



if(bar){


bar.style.width =
(strength*25)+"%";



}



});



}








// =====================================
// CONFIRM PASSWORD CHECK
// =====================================


const confirmPassword =
document.getElementById(
"confirm_password"
);



if(confirmPassword){



confirmPassword.addEventListener(
"input",
function(){



if(password.value !== this.value){


this.style.borderColor="red";


}

else{


this.style.borderColor="green";


}



});



}








// =====================================
// REGISTER VALIDATION
// =====================================


const form =
document.querySelector(
"form"
);



if(form){



form.addEventListener(

"submit",

function(e){



let name =
document.querySelector(
'input[name="name"]'
);



if(name && name.value.length < 3){



e.preventDefault();


showError(
"Ism kamida 3 ta harf bo'lishi kerak"
);


return false;


}





let pass =
document.getElementById(
"password"
).value;



let confirm =
document.getElementById(
"confirm_password"
).value;



if(pass !== confirm){



e.preventDefault();


showError(
"Parollar bir xil emas!"
);



return false;


}





let phone =
phoneInput.value.replace(/\D/g,'');



if(phone.length!==9){



e.preventDefault();



showError(
"Telefon raqam noto'g'ri"
);



return false;


}





const btn =
document.querySelector(
".register-btn"
);



if(btn){


btn.innerHTML =
"⏳ Yaratilmoqda...";


btn.disabled=true;


}



});



}








// =====================================
// ERROR MESSAGE
// =====================================


function showError(text){



let box =
document.querySelector(
".js-error"
);



if(!box){



box=document.createElement(
"div"
);



box.className=
"alert danger js-error";



document
.querySelector(".auth-card")
.prepend(box);



}



box.innerHTML=text;



box.classList.add(
"shake"
);



setTimeout(()=>{


box.classList.remove(
"shake"
);



},500);



}








// =====================================
// PASSWORD CAPSLOCK
// =====================================


if(password){


password.addEventListener(
"keyup",
function(e){



if(e.getModifierState &&
e.getModifierState("CapsLock")){


showError(
"⚠️ CapsLock yoqilgan"
);



}



});


}








// =====================================
// AUTO FOCUS
// =====================================


window.addEventListener(
"load",
()=>{


if(name){

name.focus();

}


});