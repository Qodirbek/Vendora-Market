const search =
document.getElementById("userSearch");


search.addEventListener(
"keyup",
function(){

let value =
this.value.toLowerCase();


let rows =
document.querySelectorAll(
"#usersTable tbody tr"
);



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