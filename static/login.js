function auth(event) {
    event.preventDefault(); // Prevent the default form submission behavior
  
    // Get the username and password entered by the user
    var usernameInput = document.getElementById('Username').value;
    var passwordInput = document.getElementById('password').value;
  
    // Define the allowed users and their passwords
    var allowedUsers = {
      'user1': 'user1',
      'user2': 'user2',
      'user3': 'user3',
      'user4': 'user4'
    };
  
    // Check if the entered username is valid
    if (allowedUsers.hasOwnProperty(usernameInput)) {
      // Check if the entered password matches the corresponding username
      if (passwordInput === allowedUsers[usernameInput]) {
        // Redirect to the dashboard if authentication is successful
        window.location.href = '/route_to_dashboard';
      } else {
        alert('Incorrect password. Please try again.');
      }
    } else {
      alert('Invalid username. Please enter a valid username.');
    }
  }
  