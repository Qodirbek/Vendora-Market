// =====================================
// PASSWORD SHOW / HIDE
// =====================================

function togglePassword(){

    const password =
    document.getElementById("password");


    const eye =
    document.querySelector(
        ".show-password"
    );


    if(!password) return;


    if(password.type === "password"){

        password.type="text";

        if(eye)
            eye.innerHTML="🙈";

    }

    else{


        password.type="password";


        if(eye)
            eye.innerHTML="👁";

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


// 998 ni olib tashlash

if(value.startsWith("998")){

    value=value.substring(3);

}



// faqat 9 raqam

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
// PHONE VALIDATION
// =====================================


function checkPhone(){


if(!phoneInput)
return true;



let phone =
phoneInput.value.replace(/\D/g,'');



if(phone.length!==9){


showError(
"Telefon raqam noto'g'ri"
);


return false;


}



return true;


}






// =====================================
// FORM LOADING
// =====================================


const loginForm =
document.querySelector("form");



if(loginForm){



loginForm.addEventListener(

"submit",

function(e){



if(!checkPhone()){


e.preventDefault();

return;


}



const btn =
document.querySelector(
".login-btn"
);



if(btn){


btn.innerHTML =
"⏳ Tekshirilmoqda...";


btn.disabled=true;



}



}



);


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
// CAPS LOCK CHECK
// =====================================


const password =
document.getElementById(
"password"
);



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
// OTP LOGIN READY
// =====================================


function sendOTP(){


alert(
"📩 Tasdiqlash kodi yuborish tizimi tayyor"
);



/*

Keyin:

1. Telefon yuboriladi
2. Backend OTP yaratadi
3. Telegram/SMS yuboradi
4. Kod tekshiriladi


*/


}








// =====================================
// AUTO FOCUS
// =====================================


window.addEventListener(
"load",
()=>{


if(phoneInput){

phoneInput.focus();

}


});