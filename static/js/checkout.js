console.log("CHECKOUT JS ISHLADI");
// =================================
// CHECKOUT JS
// =================================


// ================================
// PHONE FORMAT
// ================================

const phoneInput =
document.getElementById("phone");


if(phoneInput){


phoneInput.addEventListener(
"input",
function(){


let value =
this.value.replace(/\D/g,"");


// 998 ni olib tashlash

if(value.startsWith("998")){

value=value.substring(3);

}


// 9 raqamdan oshmasin

value=value.substring(0,9);



let result="+998 ";



if(value.length>0){

result += value.substring(0,2);

}


if(value.length>=3){

result += " " + value.substring(2,5);

}


if(value.length>=6){

result += " " + value.substring(5,7);

}


if(value.length>=8){

result += " " + value.substring(7,9);

}



this.value=result;


});


}



// ================================
// ADDRESS AUTO CREATE
// ================================


const form =
document.getElementById(
"checkoutForm"
);



if(form){


form.addEventListener(
"submit",
function(e){



// PHONE CHECK


let phone =
phoneInput.value;



if(phone.length < 17){


e.preventDefault();


alert(
"📱 Telefon raqamni to'liq kiriting"
);


return;


}




// ADDRESS GENERATOR


let region =
document.querySelector(
"[name='region']"
)?.value || "";


let city =
document.querySelector(
"[name='city']"
)?.value || "";


let mahalla =
document.querySelector(
"[name='mahalla']"
)?.value || "";


let street =
document.querySelector(
"[name='street']"
)?.value || "";


let house =
document.querySelector(
"[name='house']"
)?.value || "";



let apartment =
document.querySelector(
"[name='apartment']"
)?.value || "";



let fullAddress =

`${region}, ${city}, ${mahalla}, ${street}, Uy: ${house}, Xonadon: ${apartment}`;



let addressBox =
document.getElementById(
"fullAddress"
);



if(addressBox){

addressBox.value =
fullAddress;

}




// BUTTON LOADING


const btn =
document.querySelector(
".submit-btn"
);



if(btn){


btn.innerHTML =
"⏳ Buyurtma yuborilmoqda...";


btn.disabled=true;


}



});


}





// ================================
// DELIVERY PRICE UPDATE
// ================================


const deliveryInputs =
document.querySelectorAll(
"input[name='delivery_price']"
);



deliveryInputs.forEach(item=>{


item.addEventListener(
"change",
function(){


console.log(
"Yetkazib berish:",
this.value
);


});


});