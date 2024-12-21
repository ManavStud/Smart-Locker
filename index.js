const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');
const forgotPasswordBtn = document.getElementById('forgot-password-btn');
const sendOTPBtn = document.getElementById('sendOTP');
const submitResetOTPBtn = document.getElementById('submitOTP');
const verifyBtn = document.getElementById('verify');
const resendRegisterOTPBtn = document.getElementById('resendRegisterOTP');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
    container.classList.remove("active-forgot");
    container.classList.remove("active-signup")
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
    container.classList.remove("active-forgot");
    container.classList.remove("active-reset");
    container.classList.remove("active-otp-register");
    container.classList.remove("active-otp-reset");
    container.classList.remove("active-reset-password");
    container.classList.remove("active-signin")
});	

forgotPasswordBtn.addEventListener('click', () => {
    container.classList.add("active");
    container.classList.add("active-forgot");
    container.classList.add("active-signin")
    container.classList.add("active-signup")
});

// OTP for Reset Password
sendOTPBtn.addEventListener('click', (event) => {
    event.preventDefault();
    container.classList.remove("active");
    container.classList.remove("active-forgot"); // Remove forgot-password state
    container.classList.add("active-otp-reset"); // Activate Reset OTP form
    container.classList.add("active-signin")
});

// Resend OTP for Registration
resendRegisterOTPBtn.addEventListener('click', (event) => {
    event.preventDefault();
});

// Submit OTP for Reset Password
submitResetOTPBtn.addEventListener('click', (event) => {
    event.preventDefault();
    container.classList.add("active");
    container.classList.remove("active-otp-reset"); // Move to the next state
    container.classList.add("active-reset-password"); // Activate Reset Password form
});

// OTP for Registration
verifyBtn.addEventListener('click', (event) => {
    event.preventDefault();
    container.classList.remove("active"); // Remove other states
    container.classList.add("active-otp-register"); // Activate Registration OTP form
    container.classList.add("active-signin")
});