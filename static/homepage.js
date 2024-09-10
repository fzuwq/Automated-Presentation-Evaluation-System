const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');

const btnPopup = document.querySelector('.btnLogin-popup');
const iconClose = document.querySelector('.icon-close');

registerLink.addEventListener('click', ()=> {
    wrapper.classList.add('active');
});

loginLink.addEventListener('click', ()=> {
    wrapper.classList.remove('active');
});

btnPopup.addEventListener('click', ()=> {
    wrapper.classList.add('active-popup');
});

iconClose.addEventListener('click', ()=> {
    wrapper.classList.remove('active-popup');
});
// Function to submit form data via fetch and handle responses
async function submitForm(url, formData) {
    const response = await fetch(url, {
        method: 'POST',
        body: formData
    });

    return response;
}

// Event listener for registration form submission
document.querySelector('.form-box.register form').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent default form submission
    const formData = new FormData(event.target); // Get form data
    const registerUrl = '/'; // Endpoint for registration (same as current route)

    const response = await submitForm(registerUrl, formData);

    if (!response) {
        alert('An error occurred while processing your request.');
        return;
    }

    const responseData = await response.text();

    console.log('Response Status:', response.status);
    console.log('Response Data:', responseData);

    if (response.status === 200) {
        alert('User Registered Successfully. You can now Login.');
    } else if (response.status === 400 && responseData.includes('Email already exists')) {
        alert('Email already exists. Please use a different email.');
    } else {
        console.error('Unexpected response status:', response.status);
        alert('An error occurred while processing your request.');
    }
});

// Event listener for login form submission
document.querySelector('.form-box.login form').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent default form submission
    const formData = new FormData(event.target); // Get form data
    const loginUrl = '/'; // Endpoint for login (same as current route)

    const response = await submitForm(loginUrl, formData);

    if (response.ok && response.status === 200) {
        window.location.href = '/dashboard'; // Redirect to dashboard on successful login
    } else if (response.status === 401) {
        alert('Invalid Email or Password. Please Register first.');
    } else {
        console.error('Unexpected response status:', response.status);
        alert('An error occurred while processing your request.');
    }
});



document.addEventListener('DOMContentLoaded', function() {
    const loginButton = document.getElementById('loginButton');
    const closeButton = document.getElementById('icon-close');
    const centerBox = document.getElementById('center-box');

    loginButton.addEventListener('click', function() {
        centerBox.style.display = 'none';
    });

    closeButton.addEventListener('click', function() {
        centerBox.style.display = 'block';
    });
});


// Set initial value of password input to empty string
const passwordInput = document.getElementById("password");
passwordInput.value = "";

document.addEventListener("DOMContentLoaded", function () {
    const confirmPasswordInput = document.getElementById("confirmPassword");
    const matchIcon = document.getElementById("passwordMatchIcon");

    function checkPasswordMatch() {
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;

        if (password === confirmPassword && password !== "" && confirmPassword !== "") {
            matchIcon.style.color = "green";
            matchIcon.innerHTML = "&#10004;"; // Green tick symbol
        } else {
            matchIcon.style.color = "red"; // Reset color if passwords don't match or fields are empty
            matchIcon.innerHTML = "&#10005"; // red cross 
        }
    }

    // Set initial value of confirm password input to empty string
    confirmPasswordInput.value = "";

    // Add event listener to the password field for the 'input' event
    passwordInput.addEventListener("input", function () {
        // Execute checkPasswordMatch only when the user enters data into the password field
        if (passwordInput.value !== "") {
            checkPasswordMatch();
        }
    });

    // Add event listeners to both password and confirm password fields to check for matching passwords
    confirmPasswordInput.addEventListener("input", checkPasswordMatch);
});

    

  
const mobileNumberInput = document.getElementById("mobileNumber");
const mobileNumberValidationIcon = document.getElementById("mobileNumberValidationIcon");

// Add event listener to the mobile number input field for the 'input' event
mobileNumberInput.addEventListener("input", function () {
    let inputValue = mobileNumberInput.value;

    // Remove any non-numeric characters from the input value
    inputValue = inputValue.replace(/\D/g, "");

    // Limit the input value to a maximum of 10 digits
    inputValue = inputValue.slice(0, 10);

    // Update the value of the input field to display only the numeric characters up to 10 digits
    mobileNumberInput.value = inputValue;

    // Check if the input length is exactly 10 digits
    const isValidLength = inputValue.length === 10;

    // Update the display of the validation icon based on input length validity
    if (isValidLength) {
        // If input length is valid, display a green tick symbol
        mobileNumberValidationIcon.style.color = "green";
        mobileNumberValidationIcon.innerHTML = "&#10004;";
    } else {
        // If input length is invalid, display a red cross symbol
        mobileNumberValidationIcon.style.color = "red";
        mobileNumberValidationIcon.innerHTML = "&#10005;";
    }
});

