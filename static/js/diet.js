// Wait for the entire page to load
document.addEventListener("DOMContentLoaded", function() {

    // 1. Find the elements
    const dietForm = document.getElementById("get-diet-form");
    const planContainer = document.getElementById("diet-plan-container");

    // 2. Listen for the form submission
    dietForm.addEventListener("submit", function(event) {
        // Prevent the page from reloading
        event.preventDefault();

        // 3. Get the data from the form
        const age = document.getElementById("age").value;
        const gender = document.getElementById("gender").value;
        const preference = document.getElementById("preference").value;

        // 4. Create the data object to send to the backend
        const requestData = {
            age: parseInt(age),
            gender: gender,
            preference: preference,
            restrictions: [] // We can add this later if needed
        };

        // 5. Send the data to the API
        fetch("/api/diet/plan", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(requestData),
        })
        .then(response => response.json())
        .then(plan => {
            
            // 6. Clear the container and display the plan
            planContainer.innerHTML = ''; // Clear the "Your plan will appear here" text

            if (plan.error) {
                planContainer.innerHTML = `<p>Error: ${plan.error}</p>`;
                return;
            }

            // --- THIS IS THE FIX ---
            // We create an array to force the correct order
            const dayOrder = [
                "Monday", 
                "Tuesday", 
                "Wednesday", 
                "Thursday", 
                "Friday", 
                "Saturday", 
                "Sunday"
            ];

            // Loop through our ordered array, not the random object keys
            dayOrder.forEach(day => {
                
                // Check if this day exists in the plan
                if (plan[day]) {
                    const meals = plan[day]; // 'meals' will be {Breakfast: ..., Lunch: ...}

                    // Create the HTML elements for this day
                    const dayCard = document.createElement('div');
                    dayCard.className = 'day-plan';

                    const dayTitle = document.createElement('h3');
                    dayTitle.textContent = day;
                    dayCard.appendChild(dayTitle);

                    const mealList = document.createElement('ul');

                    // --- FIX #2 ---
                    // Also force the meal order
                    const mealOrder = ["Breakfast", "Lunch", "Dinner", "total_calories"];

                    mealOrder.forEach(mealName => {
                        if (meals[mealName]) {
                            const mealDescription = meals[mealName];
                            
                            const mealItem = document.createElement('li');
                            
                            if (mealName === "total_calories") {
                                mealItem.innerHTML = `<strong>Total:</strong> ${mealDescription} kcal`;
                            } else {
                                mealItem.innerHTML = `<strong>${mealName}:</strong> ${mealDescription}`;
                            }
                            mealList.appendChild(mealItem);
                        }
                    });
                    
                    dayCard.appendChild(mealList);
                    planContainer.appendChild(dayCard);
                }
            });
        })
        .catch(error => {
            console.error("Error:", error);
            planContainer.innerHTML = `<p>An error occurred. See console for details.</p>`;
        });
    });

});