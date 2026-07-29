// PASSWORD SHOW

function togglePassword(){

const password =
document.getElementById("password");

const eye =
document.querySelector(".show-password");


if(password.type==="password"){

password.type="text";

eye.innerHTML="🙈";

}

else{

password.type="password";

eye.innerHTML="👁";

}

}




// PHONE FORMAT

const phoneInput =
document.querySelector(
'input[name="phone"]'
);


if(phoneInput){


phoneInput.addEventListener(
"input",
function(){


let value=this.value.replace(/\D/g,'');


if(value.startsWith("998")){

value=value.substring(3);

}


value=value.substring(0,9);


let result="";


if(value.length>0){

result=value.substring(0,2);

}


if(value.length>=3){

result+=" "+value.substring(2,5);

}


if(value.length>=6){

result+=" "+value.substring(5,7);

}


if(value.length>=8){

result+=" "+value.substring(7,9);

}



this.value=result;



});

}




// BUTTON LOADING


const form=document.querySelector("form");


if(form){


form.addEventListener(
"submit",
()=>{


const btn=
document.querySelector(
".login-btn"
);


if(btn){

btn.innerHTML="⏳ Tekshirilmoqda...";

btn.disabled=true;

}



});


}