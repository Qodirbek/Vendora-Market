/* =====================================
        VENDORA TELEGRAM AUTH JS
===================================== */


document.addEventListener(
"DOMContentLoaded",
()=>{


console.log(
"Vendora Telegram Auth JS loaded ✅"
);



/* =====================================
        PHONE FORMAT
===================================== */


const phone =
document.querySelector(
'input[name="phone"]'
);



if(phone){


phone.addEventListener(
"input",
()=>{


let value =
phone.value.replace(
/\D/g,
''
);



/*
UZBEKISTAN FORMAT

95 461 02 06

*/

value =
value.substring(
0,
9
);



let result="";



if(value.length>0){

result =
value.substring(
0,
2
);

}



if(value.length>=3){

result +=
" "
+
value.substring(
2,
5
);

}



if(value.length>=6){

result +=
" "
+
value.substring(
5,
7
);

}



if(value.length>=8){

result +=
" "
+
value.substring(
7,
9
);

}



phone.value=result;



});



}





/* =====================================
        PASSWORD SHOW / HIDE
===================================== */


window.showPassword =
function(){


const password =
document.getElementById(
"password"
);



const button =
document.querySelector(
".password-box button"
);



if(!password)
return;



if(password.type==="password"){


password.type="text";


if(button){

button.innerHTML="🙈";

}



}


else{


password.type="password";


if(button){

button.innerHTML="👁";

}


}



};







/* =====================================
        LOGIN LOADING
===================================== */


const form =
document.querySelector(
"form"
);



const submit =
document.querySelector(
".submit"
);





if(form && submit){



form.addEventListener(
"submit",
(e)=>{


if(submit.dataset.loading==="true"){


e.preventDefault();

return;


}



submit.dataset.loading="true";



submit.innerHTML =
`
<span class="loader"></span>
 Kirilmoqda...
`;



submit.style.opacity="0.8";

submit.style.cursor="wait";



});



}







/* =====================================
        AUTO FOCUS PASSWORD
===================================== */


const passwordInput =
document.getElementById(
"password"
);



if(passwordInput){


setTimeout(
()=>{


passwordInput.focus();


},
500
);


}







/* =====================================
        TELEGRAM WEB APP
===================================== */


if(
window.Telegram &&
Telegram.WebApp
){


console.log(
"Telegram WebApp detected ✅"
);



Telegram.WebApp.ready();



Telegram.WebApp.expand();



}

else{


console.log(
"Browser mode"
);


}





});