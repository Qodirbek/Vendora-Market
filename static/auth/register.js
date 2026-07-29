function togglePassword(id){

    const password =
    document.getElementById(id);


    if(password.type==="password"){

        password.type="text";

    }

    else{

        password.type="password";

    }

}





/* Telefon formatlash */

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



if(value.length>9){

    value=value.substring(0,9);

}



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






/* Parol tekshirish */

const form =
document.querySelector("form");



if(form){


form.addEventListener(
"submit",
function(e){



const pass =
document.getElementById(
"password"
).value;



const confirm =
document.getElementById(
"confirm_password"
).value;



if(pass !== confirm){


e.preventDefault();



alert(
"Parollar bir xil emas!"
);


return false;

}





const btn =
document.querySelector(
".register-btn"
);



if(btn){

btn.innerHTML=
"⏳ Yaratilmoqda...";


btn.disabled=true;


}



});


}