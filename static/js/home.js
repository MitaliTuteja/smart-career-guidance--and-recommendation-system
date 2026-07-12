// ===============================
// SMART CAREER GUIDANCE SYSTEM
// Home Page JavaScript
// ===============================

// Wait until page is fully loaded
document.addEventListener("DOMContentLoaded", function () {

    // ===============================
    // Navbar Scroll Effect
    // ===============================

    const navbar = document.querySelector(".navbar");

    window.addEventListener("scroll", function () {

        if (window.scrollY > 50) {

            navbar.style.background = "#0F172A";
            navbar.style.boxShadow = "0 4px 15px rgba(0,0,0,0.15)";

        } else {

            navbar.style.background = "transparent";
            navbar.style.boxShadow = "none";

        }

    });

    // ===============================
    // Smooth Scroll to Features
    // ===============================

    const featureBtn = document.querySelector(".secondary-btn");
    const featureSection = document.querySelector(".features");

    if (featureBtn && featureSection) {

        featureBtn.addEventListener("click", function () {

            featureSection.scrollIntoView({
                behavior: "smooth"
            });

        });

    }

    // ===============================
    // Get Started Button
    // ===============================

    const startBtn = document.querySelector(".primary-btn");

    if (startBtn) {

        startBtn.addEventListener("click", function () {

            // Change this later when login page is ready
            window.location.href = "login.html";

        });

    }

    // ===============================
    // Login Button
    // ===============================

    const loginBtn = document.querySelector(".login-btn");

    if (loginBtn) {

        loginBtn.addEventListener("click", function () {

            window.location.href = "login.html";

        });

    }

    // ===============================
    // Sign Up Button
    // ===============================

    const signupBtn = document.querySelector(".signup-btn");

    if (signupBtn) {

        signupBtn.addEventListener("click", function () {

            window.location.href = "register.html";

        });

    }

    // ===============================
    // Feature Card Hover Animation
    // ===============================

    const cards = document.querySelectorAll(".feature-card");

    cards.forEach(card => {

        card.addEventListener("mouseenter", function () {

            card.style.transform = "translateY(-10px)";
            card.style.transition = "0.3s";

        });

        card.addEventListener("mouseleave", function () {

            card.style.transform = "translateY(0px)";

        });

    });

});