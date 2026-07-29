const search =
document.getElementById("orderSearch");


if(search){

search.addEventListener(
"keyup",
()=>{


let value =
search.value.toLowerCase();


document
.querySelectorAll(".order-card")
.forEach(card=>{


if(card.innerText
.toLowerCase()
.includes(value)){


card.style.display="block";


}else{


card.style.display="none";


}


});


});


}