document.addEventListener("DOMContentLoaded", function(){

    const menuBtn = document.querySelector(".mobile-menu-btn");
    const sidebar = document.querySelector(".sidebar");
    const overlay = document.querySelector(".sidebar-overlay");


    if(menuBtn && sidebar && overlay){

        menuBtn.addEventListener("click", function(){

            sidebar.classList.toggle("active");
            overlay.classList.toggle("active");

        });


        overlay.addEventListener("click", function(){

            sidebar.classList.remove("active");
            overlay.classList.remove("active");

        });

    }

});