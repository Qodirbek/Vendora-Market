document.querySelectorAll(".heart")
.forEach(btn=>{


btn.onclick=function(){


let id=this.dataset.id;


fetch("/favorite/toggle/"+id,{
method:"POST"
})


.then(res=>res.json())


.then(data=>{


if(!data.favorite){


let card=document.getElementById(
"favorite-"+id
);


card.style.opacity="0";

card.style.transform="scale(.8)";


setTimeout(()=>{

card.remove();


},300);


}



})


}


});





document.querySelectorAll(".delete")
.forEach(btn=>{


btn.onclick=function(){


let id=this.dataset.id;


if(!confirm("O'chirilsinmi?"))
return;



fetch("/favorite/remove/"+id,{
method:"POST"
})


.then(()=>{


this.closest(".favorite-card").remove();


});


}


});