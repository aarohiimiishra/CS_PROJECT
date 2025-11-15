document.addEventListener("DOMContentLoaded", function() {

    const registerForm = document.getElementById("register-form");
    const messageArea = document.getElementById("auth-message");

    registerForm.addEventListener("submit", function(event) {
        event.preventDefault(); // Stop the form from reloading the page

        // 1. Get all the values from the form
        const name = document.getElementById("name").value;
        const email = document.getElementById("email").value;
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        const dob = document.getElementById("dob").value; // Will be "YYYY-MM-DD"
        const height = document.getElementById("height").value;
        const weight = document.getElementById("weight").value;

        // 2. Create the data object (must match app.py)
        const registrationData = {
            name: name,
            email: email,
            username: username,
            password: password,
            date_of_birth: dob,
            height_cm: parseInt(height),
            weight_kg: parseFloat(weight)
        };

        // 3. Send the data to the /api/register endpoint
        fetch("/api/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(registrationData),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data); // Log the response from the server

            if (data.user_id) {
                // Success!
                messageArea.textContent = "Registration successful! You can now log in.";
                messageArea.className = "message-success";
                registerForm.reset(); // Clear the form
            } else {
                // Failure (e.g., "Email or Username already registered")
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