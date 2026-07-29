document.addEventListener(
"DOMContentLoaded",
()=>{


const search =
document.getElementById(
"sellerSearch"
);


const rows =
document.querySelectorAll(
"#sellerTable tbody tr"
);



search.addEventListener(
"input",
()=>{


let value =
search.value.toLowerCase();



rows.forEach(row=>{


let text =
row.innerText.toLowerCase();



if(text.includes(value)){

row.style.display="";

}

else{

row.style.display="none";

}



});


});





const buttons =
document.querySelectorAll(
".danger"
);



buttons.forEach(btn=>{


btn.addEventListener(
"click",
(e)=>{


let confirmDelete =
confirm(
"Sellerni bloklamoqchimisiz?"
);


if(!confirmDelete){

e.preventDefault();

}


});


});



});