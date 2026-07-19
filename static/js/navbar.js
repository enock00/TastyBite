/*==================================================
    TASTYBITE NAVBAR
====================================================*/

document.addEventListener("DOMContentLoaded", () => {

    /*====================================
        ELEMENTS
    ====================================*/

    const header = document.getElementById("header");

    const menuToggle = document.getElementById("menu-toggle");

    const navMenu = document.getElementById("nav-menu");

    const profileToggle = document.getElementById("profile-toggle");

    const dropdown = document.querySelector(".dropdown");

    /*====================================
        STICKY NAVBAR
    ====================================*/

    function updateNavbar() {

        if (window.scrollY > 80) {

            header.classList.add("scrolled");

        } else {

            header.classList.remove("scrolled");

        }

    }

    updateNavbar();

    window.addEventListener("scroll", updateNavbar);

    /*====================================
        MOBILE MENU
    ====================================*/

    if (menuToggle && navMenu) {

        menuToggle.addEventListener("click", () => {

            navMenu.classList.toggle("active");

            menuToggle.classList.toggle("active");

            document.body.classList.toggle("menu-open");

        });

    }

    /*====================================
        CLOSE MENU AFTER CLICK
    ====================================*/

    const navLinks = document.querySelectorAll(".nav-list a");

    navLinks.forEach(link => {

        link.addEventListener("click", () => {

            navMenu.classList.remove("active");

            menuToggle.classList.remove("active");

            document.body.classList.remove("menu-open");

        });

    });

    /*====================================
        CLICK OUTSIDE MENU
    ====================================*/

    document.addEventListener("click", (e) => {

        if (

            navMenu &&
            menuToggle &&
            !navMenu.contains(e.target) &&
            !menuToggle.contains(e.target)

        ) {

            navMenu.classList.remove("active");

            menuToggle.classList.remove("active");

            document.body.classList.remove("menu-open");

        }

    });

    /*====================================
        PROFILE DROPDOWN
    ====================================*/

    if (profileToggle && dropdown) {

        profileToggle.addEventListener("click", (e) => {

            e.stopPropagation();

            dropdown.classList.toggle("show");

        });

        document.addEventListener("click", () => {

            dropdown.classList.remove("show");

        });

    }

    /*====================================
        ACTIVE LINK ON SCROLL
    ====================================*/

    const sections = document.querySelectorAll("section[id]");

    window.addEventListener("scroll", () => {

        let current = "";

        sections.forEach(section => {

            const top = section.offsetTop - 120;

            const height = section.offsetHeight;

            if (window.scrollY >= top && window.scrollY < top + height) {

                current = section.getAttribute("id");

            }

        });

        navLinks.forEach(link => {

            link.classList.remove("active-scroll");

            const href = link.getAttribute("href");

            if (href === "#" + current) {

                link.classList.add("active-scroll");

            }

        });

    });

    /*====================================
        SEARCH ANIMATION
    ====================================*/

    const searchInput = document.querySelector(".search-box input");

    if (searchInput) {

        searchInput.addEventListener("focus", () => {

            searchInput.parentElement.classList.add("focused");

        });

        searchInput.addEventListener("blur", () => {

            searchInput.parentElement.classList.remove("focused");

        });

    }

});