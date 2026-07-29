// =====================================
// SOTUV ADMIN PANEL PRO JS
// =====================================


console.log("🚀 SOTUV Admin Panel PRO ishga tushdi");




// =====================================
// DOM READY
// =====================================

document.addEventListener(
"DOMContentLoaded",
()=>{


// FLASH AUTO HIDE

document.querySelectorAll(".alert")
.forEach(alert=>{


setTimeout(()=>{


alert.classList.add("hide");


setTimeout(()=>{

alert.remove();

},500);


},4000);


});





// FORM LOADING

document.querySelectorAll("form")
.forEach(form=>{


form.addEventListener(
"submit",
()=>{


let btn =
form.querySelector(
"button[type='submit']"
);


if(btn){


btn.dataset.old =
btn.innerHTML;


btn.innerHTML =
`
<span class="loader"></span>
Yuklanmoqda...
`;


btn.disabled=true;


}


});


});





// TABLE SEARCH

let search =
document.getElementById(
"search"
);


if(search){


search.addEventListener(
"keyup",
()=>{


let value =
search.value.toLowerCase();


document
.querySelectorAll(
"table tbody tr"
)
.forEach(row=>{


row.style.display =
row.innerText
.toLowerCase()
.includes(value)
?
""
:
"none";



});


});


}



});








// =====================================
// DELETE CONFIRM PRO
// =====================================

function confirmDelete(){


return confirm(
"⚠️ Ushbu ma'lumot o'chiriladi.\n\nDavom etasizmi?"
);


}








// =====================================
// SIDEBAR MOBILE
// =====================================

function toggleSidebar(){


let sidebar =
document.querySelector(
".sidebar"
);


let overlay =
document.querySelector(
".sidebar-overlay"
);



if(sidebar){


sidebar.classList.toggle(
"active"
);


}


if(overlay){


overlay.classList.toggle(
"show"
);


}


}








// =====================================
// NOTIFICATION SHAKE
// =====================================


function animateNotification(){


let bell =
document.querySelector(
".notification"
);



if(!bell)
return;



bell.classList.add(
"shake"
);



setTimeout(()=>{


bell.classList.remove(
"shake"
);


},700);



}









// =====================================
// IMAGE PREVIEW PRO
// =====================================


function previewImage(event){


let file =
event.target.files[0];


let image =
document.getElementById(
"imagePreview"
);



if(
file &&
image
){


let reader =
new FileReader();



reader.onload =
function(e){


image.src =
e.target.result;


image.classList.add(
"show"
);


};



reader.readAsDataURL(file);


}



}









// =====================================
// PRICE FORMAT
// =====================================


function formatPrice(input){


let value =
input.value
.replace(/\D/g,'');



if(value){


input.value =
Number(value)
.toLocaleString(
"uz-UZ"
);


}

else{


input.value="";


}


}









// =====================================
// COPY TEXT
// =====================================


function copyText(text){


navigator.clipboard
.writeText(text)
.then(()=>{


showToast(
"✅ Nusxalandi"
);


});


}









// =====================================
// TOAST SYSTEM
// =====================================


function showToast(message){


let toast =
document.createElement(
"div"
);


toast.className =
"toast";


toast.innerHTML =
message;



document.body.appendChild(
toast
);



setTimeout(()=>{


toast.classList.add(
"show"
);


},100);



setTimeout(()=>{


toast.classList.remove(
"show"
);


setTimeout(()=>{


toast.remove();


},300);



},3000);



}









// =====================================
// NUMBER COUNTER
// =====================================


function animateNumber(element){


let target =
Number(
element.dataset.value
);



let count=0;


let speed =
target/100;



let timer =
setInterval(()=>{


count+=speed;


if(count>=target){


count=target;

clearInterval(timer);


}



element.innerHTML =
Math.floor(count)
.toLocaleString(
"uz-UZ"
);



},20);



}








document
.querySelectorAll(
".counter"
)
.forEach(
animateNumber
);








// =====================================
// BACK TO TOP
// =====================================


window.addEventListener(
"scroll",
()=>{


let btn =
document.querySelector(
".top-button"
);



if(btn){


if(
window.scrollY>300
){


btn.classList.add(
"show"
);


}

else{


btn.classList.remove(
"show"
);


}


}


});






function scrollTopPage(){


window.scrollTo({

top:0,

behavior:"smooth"

});


}