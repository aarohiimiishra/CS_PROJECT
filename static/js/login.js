document.addEventListener("DOMContentLoaded", function() {

    const loginForm = document.getElementById("login-form");
    const messageArea = document.getElementById("auth-message");

    loginForm.addEventListener("submit", function(event) {
        event.preventDefault(); // Stop the form from reloading

        // 1. Get the values
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        // 2. Create the data object (must match app.py)
        const loginData = {
            email: email,
            password: password
        };

        // 3. Send to the /api/login endpoint
        fetch("/api/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(loginData),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data); // Log the response

            if (data.user_id) {
                // --- SUCCESS! ---
                // This is the most important part.
                // We save the user's info in the browser's storage.
                localStorage.setItem("user_id", data.user_id);
                localStorage.setItem("user_name", data.name);
                
                messageArea.textContent = "Login successful! Redirecting...";
                messageArea.className = "message-success";
                
                // After 1 second, send the user to the home page
                setTimeout(() => {
                    window.location.href = "/"; // Redirect to home
                }, 1000);

            } else {
                // Failure (e.g., "Invalid email or password")
                messageArea.textContent = `Error: ${data.message}`;
                messageArea.className = "message-error";
            }
        })
        .catch(error => {
            console.error("Error:", error);
            messageArea.textContent = "An error occurred. Please try again.";
            messageArea.className = "message-error";
        });
    });

});