function addCart(id){

fetch("/cart/add/"+id)

.then(res=>{

if(res.redirected){

window.location=res.url;

}

else{

alert("🛒 Savatga qo'shildi");

}

})


}



// CTRL + ENTER qidirish

document.addEventListener(
"keydown",
function(e){

if(e.ctrlKey && e.key==="Enter"){

document.querySelector("form").submit();

}

});