console.log("CHECKOUT JS ISHLADI ✅");


// ==========================
// PHONE FORMAT
// ==========================

const phoneInput = document.getElementById("phone");

const finalPrice =
document.getElementById("finalPrice");

if(phoneInput){

phoneInput.addEventListener("input",function(){

let value=this.value.replace(/\D/g,"");


if(value.startsWith("998")){
value=value.substring(3);
}


value=value.substring(0,9);


let result="+998 ";


if(value.length>0){
result+=value.substring(0,2);
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





// ==========================
// CARD SHOW / HIDE
// ==========================


const cardRadio=document.getElementById("card");
const cashRadio=document.getElementById("cash");
const cardBox=document.getElementById("cardBox");



if(cardRadio && cashRadio && cardBox){


cardRadio.addEventListener("change",function(){

if(this.checked){

cardBox.style.display="block";

}

});



cashRadio.addEventListener("change",function(){

if(this.checked){

cardBox.style.display="none";

}

});


}





// ==========================
// COPY CARD
// ==========================


function copyCard(){


let cardNumber=document.getElementById(
"cardNumber"
);



if(cardNumber){


navigator.clipboard.writeText(
cardNumber.innerText
);


alert(
"Karta raqami nusxalandi ✅"
);


}


}







// ==========================
// DELIVERY + TOTAL CALCULATOR
// ==========================

const baseTotal = Number(
document.getElementById("baseTotal").value
);

const paymentTotal =
document.getElementById("paymentTotal");

const deliveryTotal =
document.getElementById("deliveryPrice");

const finalTotal =
document.getElementById("finalTotal");

const deliveryTypes =
document.querySelectorAll(
    "input[name='delivery_type']"
);


function calculateDelivery(){

    let delivery = 0;


    const selected =
    document.querySelector(
        "input[name='delivery_type']:checked"
    );
    let finalAmount = baseTotal + delivery;
    if(finalPrice){
    finalPrice.value = finalAmount;
    }

    if(selected){

        // KURYER
        if(selected.value === "courier"){

            if(baseTotal >= 1200000){
                delivery = 0;
            }
            else{
                delivery = 30000;
            }

        }


        // STANDART
        else{

            if(baseTotal >= 120000){
                delivery = 0;
            }

            else if(baseTotal >= 45000){
                delivery = 10000;
            }

            else if(baseTotal >= 10000){
                delivery = 20000;
            }

            else{
                delivery = 30000;
            }

        }

    }


    



    // Yetkazish narxi
    if(deliveryTotal){

        deliveryTotal.innerHTML =
        delivery.toLocaleString()
        + " so'm";

    }



    // Jami summa
    if(finalTotal){

        finalTotal.innerHTML =
        finalAmount.toLocaleString()
        + " so'm";

    }



    // Karta ichidagi summa
    if(paymentTotal){

        paymentTotal.innerHTML =
        finalAmount.toLocaleString()
        + " so'm";

    }


}



// Yetkazish tanlanganda hisoblash

deliveryTypes.forEach(
    item => {

        item.addEventListener(
            "change",
            calculateDelivery
        );

    }
);


// Sahifa ochilganda hisoblash

calculateDelivery();



// ==========================
// CHECKOUT FORM
// ==========================

const form =
document.getElementById(
    "checkoutForm"
);





if(form){

form.addEventListener(
"submit",
function(e){


    // karta bo'lsa chek tekshiradi

    if(cardRadio && cardRadio.checked){


        const file =
        document.querySelector(
            "input[name='payment_check']"
        );


        if(!file || file.files.length === 0){

            e.preventDefault();

            alert(
            "💳 Karta orqali to'lovda chek yuklash majburiy!"
            );

            return;

        }

    }



    const btn =
    document.querySelector(
        ".submit-btn"
    );


    if(btn){

        btn.innerHTML =
        "⏳ Buyurtma yuborilmoqda...";

        btn.disabled = true;

    }


});


}

const paymentFile = document.getElementById("paymentCheck");
const fileName = document.getElementById("fileName");

if(paymentFile){
    paymentFile.addEventListener("change", function(){

        if(this.files.length > 0){
            fileName.innerHTML =
            "✅ " + this.files[0].name;
        }
        else{
            fileName.innerHTML =
            "Fayl tanlanmagan";
        }

    });
}