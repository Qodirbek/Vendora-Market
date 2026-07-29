document.addEventListener(
"DOMContentLoaded",
()=>{


const rows=document.querySelectorAll(
".orders-table tbody tr"
);


rows.forEach(row=>{


row.addEventListener(
"click",
()=>{

row.style.background="#eff6ff";


setTimeout(()=>{

row.style.background="";

},500);


});


});


});