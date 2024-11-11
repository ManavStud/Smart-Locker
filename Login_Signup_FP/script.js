document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('container');
    const registerBtn = document.getElementById('register');
    const loginBtn = document.getElementById('login');
    const forgotPasswordLink = document.getElementById('forgotPasswordLink');
    const backToSignInBtn = document.getElementById('backToSignIn');

    registerBtn.addEventListener('click', () => {
        container.classList.add("active");
        container.classList.remove("active-forgot-password");
    });

    loginBtn.addEventListener('click', () => {
        container.classList.remove("active");
        container.classList.remove("active-forgot-password");
    });

    forgotPasswordLink.addEventListener('click', (event) => {
        event.preventDefault();
        container.classList.add("active-forgot-password");
    });

    backToSignInBtn.addEventListener('click', () => {
        container.classList.remove("active-forgot-password");
    });
});
