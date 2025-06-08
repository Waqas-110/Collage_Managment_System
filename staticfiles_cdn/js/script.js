// D:\YouExcel_Management_System\static\js\script.js

document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.querySelector('input[type="password"]');
    const togglePassword = document.querySelector('.icon-eye');

    if (passwordInput && togglePassword) {
        togglePassword.addEventListener('click', function() {
            // Toggle the type attribute
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);

            // You could also toggle an icon class here if you have different eye icons
            // e.g., togglePassword.classList.toggle('fa-eye-slash');
        });
    }

    console.log("script.js loaded successfully!");
});