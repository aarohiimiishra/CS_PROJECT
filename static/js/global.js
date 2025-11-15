// This script will run on every page
document.addEventListener("DOMContentLoaded", function() {

    // Find the navigation bar's list
    const navUl = document.querySelector("nav ul");
    
    // Check if a user_id is saved in the browser
    const userId = localStorage.getItem("user_id");
    const userName = localStorage.getItem("user_name");

    if (userId && userName) {
        // --- USER IS LOGGED IN ---

        // 1. Remove the old links (Home, Workouts, Diet)
        // We do this so we can add them back in the correct order
        navUl.innerHTML = ''; 

        // 2. Add back the standard links
        navUl.innerHTML += `<li><a href="/">Home</a></li>`;
        navUl.innerHTML += `<li><a href="/workout">Workouts</a></li>`;
        navUl.innerHTML += `<li><a href="/diet">Diet</a></li>`;

        // 3. Add a "Welcome" message
        const welcomeLi = document.createElement('li');
        welcomeLi.className = 'nav-welcome'; // For styling
        welcomeLi.textContent = `Welcome, ${userName}`;
        navUl.appendChild(welcomeLi);

        // 4. Add a "Logout" button
        const logoutLi = document.createElement('li');
        const logoutButton = document.createElement('a');
        logoutButton.href = "#"; // It's a button, not a link
        logoutButton.textContent = "Logout";
        logoutButton.id = "logout-button"; // We'll add a click listener
        logoutLi.appendChild(logoutButton);
        navUl.appendChild(logoutLi);

        // 5. Add click listener for the logout button
        logoutButton.addEventListener("click", function() {
            // Clear the user's info from storage
            localStorage.removeItem("user_id");
            localStorage.removeItem("user_name");
            // Send them back to the home page
            window.location.href = "/login";
        });

    } else {
        // --- USER IS LOGGED OUT ---

        // 1. Clear the nav bar
        navUl.innerHTML = '';

        // 2. Add back the standard links
        navUl.innerHTML += `<li><a href="/">Home</a></li>`;
        navUl.innerHTML += `<li><a href="/workout">Workouts</a></li>`;
        navUl.innerHTML += `<li><a href="/diet">Diet</a></li>`;

        // 3. Add "Login" and "Register" links
        navUl.innerHTML += `<li><a href="/login" class="nav-button-login">Login</a></li>`;
        navUl.innerHTML += `<li><a href="/register" class="nav-button-register">Register</a></li>`;
    }
});