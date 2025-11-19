document.addEventListener("DOMContentLoaded", function() {
    
    const planContainer = document.getElementById("workout-plan-container");
    const planInfo = document.getElementById("plan-info");

    // 1. Get User ID
    const userId = localStorage.getItem("user_id");
    if (!userId) {
        planInfo.innerHTML = "<p>Please log in to view your personalized plan.</p>";
        return;
    }

    // 2. Fetch the plan
    fetch(`/api/workout_plan/${userId}`)
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.message) });
            }
            return response.json();
        })
        .then(data => {
            // data has: { age, category, plan: { focus, plan: [] } }
            
            // 3. Display basic info
            planInfo.innerHTML = `
                <p><strong>Age:</strong> ${data.age} | <strong>Category:</strong> ${data.category.replace('_', ' ')}</p>
                <p><strong>Focus:</strong> ${data.plan.focus}</p>
                <hr>
            `;

            // 4. Display the weekly schedule
            planContainer.innerHTML = ''; // Clear loading text

            data.plan.plan.forEach(dayItem => {
                // Create a card for each day
                const dayCard = document.createElement('div');
                dayCard.className = 'day-plan';

                // Title (e.g., "Monday - Push Day")
                const title = document.createElement('h3');
                title.textContent = `${dayItem.day} - ${dayItem.type}`;
                dayCard.appendChild(title);

                const detailsList = document.createElement('ul');

                // If it has a list of exercises
                if (dayItem.exercises) {
                    dayItem.exercises.forEach(exercise => {
                        const li = document.createElement('li');
                        li.textContent = exercise;
                        detailsList.appendChild(li);
                    });
                } 
                // If it has a single activity (like cardio)
                else if (dayItem.activity) {
                    const li = document.createElement('li');
                    let text = `Activity: ${dayItem.activity}`;
                    if (dayItem.duration_min) text += ` (${dayItem.duration_min} mins)`;
                    if (dayItem.distance_km) text += ` (${dayItem.distance_km} km)`;
                    li.textContent = text;
                    detailsList.appendChild(li);
                }

                // Notes
                if (dayItem.notes) {
                    const noteLi = document.createElement('li');
                    noteLi.innerHTML = `<em>Note: ${dayItem.notes}</em>`;
                    noteLi.style.color = "#7f8c8d";
                    detailsList.appendChild(noteLi);
                }

                dayCard.appendChild(detailsList);
                planContainer.appendChild(dayCard);
            });

        })
        .catch(error => {
            console.error("Error:", error);
            planInfo.innerHTML = `<p class="message-error">Could not load plan: ${error.message}</p>`;
        });

});