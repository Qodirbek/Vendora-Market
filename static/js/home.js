
function addCart(id){

fetch("/cart/add/"+id)

.then(res=>res.json())

.then(data=>{

alert("Savatga qo'shildi");

})


}



function favorite(id){


fetch("/favorite/add/"+id)

.then(res=>res.json())

.then(data=>{

alert("Sevimlilarga qo'shildi");

})


}

document.querySelectorAll(".favorite-btn")
.forEach(btn=>{


btn.addEventListener("click",()=>{


let productId = btn.dataset.id;


fetch(
"/favorite/toggle/"+productId,
{
method:"POST",
headers:{
"Content-Type":"application/json"
}
}
)

.then(res=>res.json())

.then(data=>{


if(data.login){

alert("Avval tizimga kiring");

return;

}


if(data.favorite){

btn.classList.add("active");

btn.innerHTML="❤️";

}

else{

btn.classList.remove("active");

btn.innerHTML="🤍";

}



})


.catch(err=>{

console.log(err);

});


});


});