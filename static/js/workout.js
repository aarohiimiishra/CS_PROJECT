// Wait for the entire page to load before running any code
document.addEventListener("DOMContentLoaded", function() {
    
    // --- 1. Find elements on the page ---
    const workoutForm = document.getElementById("log-workout-form");
    const workoutsContainer = document.getElementById("logged-workouts-container");
    const noWorkoutsMessage = document.getElementById("no-workouts-message");

    
    // --- 2. Function to fetch and display all workouts ---
    function loadWorkouts() {
        
        const userId = localStorage.getItem("user_id");
        if (!userId) {
            if (workoutForm) workoutForm.style.display = 'none'; 
            noWorkoutsMessage.textContent = "Please log in to see your workouts.";
            noWorkoutsMessage.style.display = 'block';
            return; 
        }

        fetch(`/api/workouts/${userId}`) 
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { 
                        throw new Error(err.message || "Server error in get_workouts"); 
                    });
                }
                return response.json();
            })
            .then(workouts => {
                
                workoutsContainer.innerHTML = ''; 

                if (workouts.length === 0) {
                    noWorkoutsMessage.textContent = "You haven't logged any workouts yet.";
                    noWorkoutsMessage.style.display = 'block';
                } else {
                    noWorkoutsMessage.style.display = 'none';
                    workouts.forEach(workout => {
                        const item = document.createElement('div');
                        item.className = 'workout-item';
                        
                        // Create a container for the text
                        const textContainer = document.createElement('div');
                        
                        const title = document.createElement('h3');
                        title.textContent = workout.exercise_name;
                        
                        const details = document.createElement('p');
                        details.textContent = `Set: ${workout.set_number}, Reps: ${workout.reps}, Weight: ${workout.weight_kg}kg`;
                        
                        textContainer.appendChild(title);
                        textContainer.appendChild(details);

                        // --- THIS IS THE NEW PART (Adding a delete button) ---
                        const deleteButton = document.createElement('button');
                        deleteButton.className = 'button-delete';
                        deleteButton.textContent = 'Delete';
                        
                        // Store the log's ID on the button itself
                        deleteButton.dataset.logId = workout.id;
                        
                        // Add the text and the button to the item
                        item.appendChild(textContainer);
                        item.appendChild(deleteButton);
                        
                        workoutsContainer.appendChild(item);
                    });
                }
            })
            .catch(error => {
                console.error('Error loading workouts:', error);
                alert(`Error loading workout list: ${error.message}`);
            });
    }

    
    // --- 3. Add an event listener for when the form is "submitted" ---
    if (workoutForm) {
        workoutForm.addEventListener("submit", function(event) {
            event.preventDefault(); 

            const userId = localStorage.getItem("user_id");
            if (!userId) {
                alert("You must be logged in to log a workout.");
                return;
            }

            const exerciseName = document.getElementById("exercise_name").value;
            const sets = document.getElementById("sets").value;
            const reps = document.getElementById("reps").value;
            const weight = document.getElementById("weight").value || 0;

            const workoutData = {
                user_id: parseInt(userId),
                exercises: [
                    {
                        name: exerciseName,
                        sets: [
                            {
                                set_number: 1, 
                                reps: parseInt(reps),
                                weight_kg: parseFloat(weight)
                            }
                        ]
                    }
                ]
            };

            fetch("/api/workout/log_session", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(workoutData),
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { 
                        throw new Error(err.message || "Server error"); 
                    });
                }
                return response.json();
            })
            .then(data => {
                loadWorkouts(); 
                workoutForm.reset();
            })
            .catch((error) => {
                console.error("Error:", error);
                alert(`Error: ${error.message}`);
            });
        });
    }

    // --- 4. NEW: Add a listener for all "Delete" buttons ---
    // We listen on the whole container (this is called event delegation)
    workoutsContainer.addEventListener('click', function(event) {
        
        // Check if the thing we clicked was a delete button
        if (event.target.classList.contains('button-delete')) {
            
            // Get the ID we stored on the button
            const logId = event.target.dataset.logId;
            
            // Send the delete request to the backend
            fetch(`/api/workout/delete/${logId}`, {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    // Success! Reload the workout list.
                    loadWorkouts();
                } else {
                    alert('Error: ' + (data.error || 'Could not delete workout.'));
                }
            })
            .catch(error => {
                console.error('Error deleting:', error);
                alert('An error occurred while deleting.');
            });
        }
    });

    
    // --- 5. Load workouts when the page first opens ---
    loadWorkouts();

});