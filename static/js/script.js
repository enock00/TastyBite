const menu = document.getElementById("nav-menu");

const toggle = document.getElementById("menu-toggle");

toggle.addEventListener("click", () => {

    menu.classList.toggle("active");

});

// =============================
// Mobile Menu
// =============================

const menu = document.getElementById("nav-menu");
const toggle = document.getElementById("menu-toggle");

if (toggle && menu) {
    toggle.addEventListener("click", () => {
        menu.classList.toggle("active");
    });
}

// =============================
// Back To Top Button
// =============================

const backToTop = document.getElementById("backToTop");

window.addEventListener("scroll", () => {

    if(window.scrollY > 300){

        backToTop.style.display = "flex";

    }else{

        backToTop.style.display = "none";

    }

});

backToTop.addEventListener("click", ()=>{

    window.scrollTo({

        top:0,

        behavior:"smooth"

    });

});

// =============================
// Scroll Reveal Animation
// =============================

const observer = new IntersectionObserver((entries)=>{

    entries.forEach(entry=>{

        if(entry.isIntersecting){

            entry.target.classList.add("show");

        }

    });

});

document.querySelectorAll("section").forEach(section=>{

    section.classList.add("hidden");

    observer.observe(section);

});