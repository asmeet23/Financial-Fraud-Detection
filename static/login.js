// Get the login form element
const loginForm = document.querySelector('#login-form');

// Add event listener for form submission
loginForm.addEventListener('submit', (e) => {
    e.preventDefault(); // Prevent form submission

    // Get the input values
    const username = document.querySelector('#username').value;
    const password = document.querySelector('#password').value;

    // Perform login validation
    if (enteredUsername === 'admin' && enteredPassword === 'password') {
        // Successful login, redirect to another page
        window.location.href = "dashboard.html";
    } else {
        errorMessage.textContent = "Invalid username or password.";
    }
});
