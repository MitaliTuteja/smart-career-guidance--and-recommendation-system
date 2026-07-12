// ===============================
// LOGIN PAGE JAVASCRIPT
// Smart Career Guidance System
// ===============================

document.addEventListener("DOMContentLoaded", function () {

    const loginForm = document.getElementById("loginForm");
    const email = document.getElementById("email");
    const password = document.getElementById("password");
    const togglePassword = document.getElementById("togglePassword");

    loginForm.addEventListener("submit", function (event) {

        // event.preventDefault();

        // const emailValue = email.value.trim();
        // const passwordValue = password.value.trim();

        // // Empty validation
        // if (emailValue === "" || passwordValue === "") {

        //     alert("Please fill in all fields.");
        //     return;

        // }

        // // Email validation
        // const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

        // if (!emailPattern.test(emailValue)) {

        //     alert("Please enter a valid email address.");
        //     return;

        // }

        // // Password length validation
        // if (passwordValue.length < 6) {

        //     alert("Password must contain at least 6 characters.");
        //     return;

        // }

        // alert("Login Successful!");

        // Temporary redirect
        // window.location.href = "dashboard.html";


        const emailValue = email.value.trim();
        const passwordValue = password.value.trim();

        if (emailValue === "" || passwordValue === "") {
           event.preventDefault();
            alert("Please fill in all fields.");
            return;
        }

        const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

        if (!emailPattern.test(emailValue)) {
            event.preventDefault();
            alert("Please enter a valid email address.");
            return;
        }

        if (passwordValue.length < 6) {
            event.preventDefault();
            alert("Password must contain at least 6 characters.");
            return;
        }

        // Do NOT redirect here.
        // Flask will receive the form and decide what to do.

    });

    // Show / Hide Password

    togglePassword.addEventListener("click", function(){

    if(password.type === "password"){

        password.type = "text";

        togglePassword.classList.remove("fa-eye");
        togglePassword.classList.add("fa-eye-slash");

    }

    else{

        password.type = "password";

        togglePassword.classList.remove("fa-eye-slash");
        togglePassword.classList.add("fa-eye");

    }

});

});