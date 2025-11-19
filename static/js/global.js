// This script will run on every page
document.addEventListener("DOMContentLoaded", function() {

    // Find the navigation bar's list
    const navUl = document.querySelector("nav ul");
    
    // Check if a user_id is saved in the browser
    const userId = localStorage.getItem("user_id");
    const userName = localStorage.getItem("user_name");

    if (userId && userName) {
        // --- USER IS LOGGED IN ---

        // 1. Remove the old links
        navUl.innerHTML = ''; 

        // 2. Add back the standard links (INCLUDING MY PLAN)
        navUl.innerHTML += `<li><a href="/">Home</a></li>`;
        navUl.innerHTML += `<li><a href="/workout">Workouts</a></li>`;
        navUl.innerHTML += `<li><a href="/my_plan">My Plan</a></li>`; // <--- NEW LINK
        navUl.innerHTML += `<li><a href="/diet">Diet</a></li>`;

        // 3. Add a "Welcome" message
        const welcomeLi = document.createElement('li');
        welcomeLi.className = 'nav-welcome'; 
        welcomeLi.textContent = `Welcome, ${userName}`;
        navUl.appendChild(welcomeLi);

        // 4. Add a "Logout" button
        const logoutLi = document.createElement('li');
        const logoutButton = document.createElement('a');
        logoutButton.href = "#"; 
        logoutButton.textContent = "Logout";
        logoutButton.id = "logout-button"; 
        logoutLi.appendChild(logoutButton);
        navUl.appendChild(logoutLi);

        // 5. Add click listener for the logout button
        logoutButton.addEventListener("click", function() {
            localStorage.removeItem("user_id");
            localStorage.removeItem("user_name");
            window.location.href = "/login";
        });

    } else {
        // --- USER IS LOGGED OUT ---

        // 1. Clear the nav bar
        navUl.innerHTML = '';

        // 2. Add back the standard links (INCLUDING MY PLAN)
        navUl.innerHTML += `<li><a href="/">Home</a></li>`;
        navUl.innerHTML += `<li><a href="/workout">Workouts</a></li>`;
        navUl.innerHTML += `<li><a href="/my_plan">My Plan</a></li>`; // <--- NEW LINK
        navUl.innerHTML += `<li><a href="/diet">Diet</a></li>`;

        // 3. Add "Login" and "Register" links
        navUl.innerHTML += `<li><a href="/login" class="nav-button-login">Login</a></li>`;
        navUl.innerHTML += `<li><a href="/register" class="nav-button-register">Register</a></li>`;
    }
});