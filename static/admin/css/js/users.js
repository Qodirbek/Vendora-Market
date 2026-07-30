function saveConfirm(){

return confirm(
"Foydalanuvchi sozlamalari saqlansinmi?"
);

}



document.addEventListener(
"DOMContentLoaded",
()=>{


let rows=document.querySelectorAll(
"tbody tr"
);


rows.forEach(row=>{


row.addEventListener(
"mouseenter",
()=>{

row.style.background="#f8fafc";

});


row.addEventListener(
"mouseleave",
()=>{

row.style.background="";

});


});


});