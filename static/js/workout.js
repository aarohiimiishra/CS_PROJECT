// Wait for the entire page to load before running any code
document.addEventListener("DOMContentLoaded", function() {
    
    // 1. Find the form on the page
    const workoutForm = document.getElementById("log-workout-form");

    // 2. Add an event listener for when the form is "submitted"
    workoutForm.addEventListener("submit", function(event) {
        
        // 3. Prevent the page from reloading (the default action)
        event.preventDefault();

        // 4. Get the data from the form fields
        const exerciseName = document.getElementById("exercise_name").value;
        const sets = document.getElementById("sets").value;
        const reps = document.getElementById("reps").value;
        const weight = document.getElementById("weight").value || 0; // Default to 0 if empty

        // 5. We need to match the data structure your backend expects!
        // Your backend /api/workout/log_session expects a list of exercises,
        // and each exercise has a list of sets.
        const workoutData = {
            user_id: 1, // We'll hardcode user 1 for now.
            exercises: [
                {
                    name: exerciseName,
                    sets: [
                        {
                            set_number: 1, // We'll simplify for now
                            reps: parseInt(reps),
                            weight_kg: parseFloat(weight)
                        }
                        // In a real app, you'd loop from 1 to 'sets'
                    ]
                }
            ]
        };

        // 6. Send this data to the backend API
        fetch("/api/workout/log_session", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(workoutData),
        })
        .then(response => response.json())
        .then(data => {
            console.log("Success:", data);
            alert("Workout logged successfully!"); 
            // We can add the new workout to the list here later.
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("Error logging workout. See console for details.");
        });
    });

});