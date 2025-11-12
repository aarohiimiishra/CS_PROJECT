from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import datetime # Added for compatibility, though not used in core logic

# --- 2. DIET PLANS DATA (Your Partner's Logic) ---
diet_plans = {
        "1-13": {
            "male": {
                "Monday": {"Breakfast": "Milk with oats (300 kcal)", "Lunch": "Dal, rice and veggies (500 kcal)", "Dinner": "Chapati and sabzi (400 kcal)"},
                "Tuesday": {"Breakfast": "Poha with peanuts (300 kcal)", "Lunch": "Vegetable pulao (500 kcal)", "Dinner": "Idli with sambar (400 kcal)"},
                "Wednesday": {"Breakfast": "Banana smoothie (250 kcal)", "Lunch": "Paneer rice bowl (500 kcal)", "Dinner": "Khichdi (400 kcal)"},
                "Thursday": {"Breakfast": "Egg sandwich (350 kcal)", "Lunch": "Chicken curry and rice (600 kcal)", "Dinner": "Dal khichdi (400 kcal)"},
                "Friday": {"Breakfast": "Milk and cereal (300 kcal)", "Lunch": "Rajma rice (550 kcal)", "Dinner": "Chapati with veg curry (400 kcal)"},
                "Saturday": {"Breakfast": "Upma (300 kcal)", "Lunch": "Grilled fish with rice (600 kcal)", "Dinner": "Vegetable soup and bread (350 kcal)"},
                "Sunday": {"Breakfast": "Paratha with curd (350 kcal)", "Lunch": "Veg thali (550 kcal)", "Dinner": "Dosa with chutney (400 kcal)"}
            },
            "female": {
                "Monday": {"Breakfast": "Milk with oats (250 kcal)", "Lunch": "Dal, rice and veggies (450 kcal)", "Dinner": "Chapati and sabzi (350 kcal)"},
                "Tuesday": {"Breakfast": "Poha with peanuts (250 kcal)", "Lunch": "Vegetable pulao (450 kcal)", "Dinner": "Idli with sambar (350 kcal)"},
                "Wednesday": {"Breakfast": "Banana smoothie (200 kcal)", "Lunch": "Paneer rice bowl (450 kcal)", "Dinner": "Khichdi (350 kcal)"},
                "Thursday": {"Breakfast": "Egg sandwich (300 kcal)", "Lunch": "Chicken curry and rice (500 kcal)", "Dinner": "Dal khichdi (350 kcal)"},
                "Friday": {"Breakfast": "Milk and cereal (250 kcal)", "Lunch": "Rajma rice (450 kcal)", "Dinner": "Chapati with veg curry (350 kcal)"},
                "Saturday": {"Breakfast": "Upma (250 kcal)", "Lunch": "Grilled fish with rice (500 kcal)", "Dinner": "Vegetable soup and bread (300 kcal)"},
                "Sunday": {"Breakfast": "Paratha with curd (300 kcal)", "Lunch": "Veg thali (500 kcal)", "Dinner": "Dosa with chutney (350 kcal)"}
            }
        },
        "13-18": {
            "male": {
                "Monday": {"Breakfast": "Eggs and toast (400 kcal)", "Lunch": "Chicken rice bowl (750 kcal)", "Dinner": "Roti and dal (500 kcal)"},
                "Tuesday": {"Breakfast": "Paratha and curd (400 kcal)", "Lunch": "Rajma rice (700 kcal)", "Dinner": "Veg noodles (550 kcal)"},
                "Wednesday": {"Breakfast": "Poha (350 kcal)", "Lunch": "Fish and rice (750 kcal)", "Dinner": "Paneer curry and chapati (550 kcal)"},
                "Thursday": {"Breakfast": "Idli sambar (350 kcal)", "Lunch": "Veg thali (700 kcal)", "Dinner": "Soup and bread (450 kcal)"},
                "Friday": {"Breakfast": "Milk and nuts (350 kcal)", "Lunch": "Grilled chicken with rice (800 kcal)", "Dinner": "Dal khichdi (500 kcal)"},
                "Saturday": {"Breakfast": "Oats and banana (400 kcal)", "Lunch": "Veg biryani (700 kcal)", "Dinner": "Paneer wrap (500 kcal)"},
                "Sunday": {"Breakfast": "Smoothie bowl (400 kcal)", "Lunch": "Rajma rice (700 kcal)", "Dinner": "Egg curry and roti (500 kcal)"}
            },
            "female": {
                "Monday": {"Breakfast": "Eggs and toast (350 kcal)", "Lunch": "Paneer rice bowl (600 kcal)", "Dinner": "Roti and dal (400 kcal)"},
                "Tuesday": {"Breakfast": "Paratha and curd (350 kcal)", "Lunch": "Veg pulao (600 kcal)", "Dinner": "Veg noodles (400 kcal)"},
                "Wednesday": {"Breakfast": "Poha (300 kcal)", "Lunch": "Fish curry and rice (600 kcal)", "Dinner": "Paneer curry and chapati (400 kcal)"},
                "Thursday": {"Breakfast": "Idli sambar (300 kcal)", "Lunch": "Veg thali (550 kcal)", "Dinner": "Soup and salad (350 kcal)"},
                "Friday": {"Breakfast": "Milk and nuts (300 kcal)", "Lunch": "Chicken with rice (650 kcal)", "Dinner": "Dal khichdi (400 kcal)"},
                "Saturday": {"Breakfast": "Oats and banana (350 kcal)", "Lunch": "Veg biryani (600 kcal)", "Dinner": "Paneer wrap (400 kcal)"},
                "Sunday": {"Breakfast": "Smoothie bowl (350 kcal)", "Lunch": "Rajma rice (600 kcal)", "Dinner": "Egg curry and roti (400 kcal)"}
            }
        },
        "18-35": {
            "male": {
                "Monday": {"Breakfast": "Oats and banana smoothie (400 kcal)", "Lunch": "Grilled chicken and rice (750 kcal)", "Dinner": "Brown rice and lentils (600 kcal)"},
                "Tuesday": {"Breakfast": "Eggs and toast (450 kcal)", "Lunch": "Paneer curry with rice (700 kcal)", "Dinner": "Vegetable pulao (550 kcal)"},
                "Wednesday": {"Breakfast": "Upma (400 kcal)", "Lunch": "Fish and rice (750 kcal)", "Dinner": "Chapati and dal (500 kcal)"},
                "Thursday": {"Breakfast": "Paratha and curd (450 kcal)", "Lunch": "Veg thali (700 kcal)", "Dinner": "Soup and bread (500 kcal)"},
                "Friday": {"Breakfast": "Milk and nuts (400 kcal)", "Lunch": "Chicken curry and rice (800 kcal)", "Dinner": "Grilled paneer salad (500 kcal)"},
                "Saturday": {"Breakfast": "Idli sambar (400 kcal)", "Lunch": "Veg noodles (700 kcal)", "Dinner": "Khichdi (500 kcal)"},
                "Sunday": {"Breakfast": "Smoothie bowl (450 kcal)", "Lunch": "Rajma rice (700 kcal)", "Dinner": "Egg curry and chapati (550 kcal)"}
            },
            "female": {
                "Monday": {"Breakfast": "Oats and milk (300 kcal)", "Lunch": "Grilled chicken and vegetables (600 kcal)", "Dinner": "Brown rice and dal (500 kcal)"},
                "Tuesday": {"Breakfast": "Egg and toast (350 kcal)", "Lunch": "Paneer wrap (550 kcal)", "Dinner": "Vegetable pulao (450 kcal)"},
                "Wednesday": {"Breakfast": "Poha (300 kcal)", "Lunch": "Fish curry and rice (600 kcal)", "Dinner": "Roti and sabzi (400 kcal)"},
                "Thursday": {"Breakfast": "Paratha and curd (350 kcal)", "Lunch": "Veg thali (550 kcal)", "Dinner": "Soup and salad (400 kcal)"},
                "Friday": {"Breakfast": "Milk and fruits (300 kcal)", "Lunch": "Chicken curry and rice (650 kcal)", "Dinner": "Paneer salad (400 kcal)"},
                "Saturday": {"Breakfast": "Idli sambar (300 kcal)", "Lunch": "Veg noodles (550 kcal)", "Dinner": "Khichdi (400 kcal)"},
                "Sunday": {"Breakfast": "Smoothie bowl (350 kcal)", "Lunch": "Rajma rice (600 kcal)", "Dinner": "Egg curry and chapati (450 kcal)"}
            }
        },
        "35-50": {
            "male": {
                "Monday": {"Breakfast": "Vegetable upma (350 kcal)", "Lunch": "Grilled fish with rice (700 kcal)", "Dinner": "Chapati and dal (500 kcal)"},
                "Tuesday": {"Breakfast": "Oats and milk (350 kcal)", "Lunch": "Chicken curry with rice (700 kcal)", "Dinner": "Vegetable soup and bread (400 kcal)"},
                "Wednesday": {"Breakfast": "Poha (300 kcal)", "Lunch": "Paneer rice (650 kcal)", "Dinner": "Roti and sabzi (400 kcal)"},
                "Thursday": {"Breakfast": "Paratha and curd (350 kcal)", "Lunch": "Veg thali (650 kcal)", "Dinner": "Soup and salad (400 kcal)"},
                "Friday": {"Breakfast": "Milk and nuts (300 kcal)", "Lunch": "Grilled chicken with rice (700 kcal)", "Dinner": "Khichdi (400 kcal)"},
                "Saturday": {"Breakfast": "Idli sambar (300 kcal)", "Lunch": "Veg noodles (650 kcal)", "Dinner": "Dal and rice (400 kcal)"},
                "Sunday": {"Breakfast": "Smoothie bowl (350 kcal)", "Lunch": "Rajma rice (650 kcal)", "Dinner": "Egg curry and chapati (400 kcal)"}
            },
            "female": {
                "Monday": {"Breakfast": "Vegetable upma (300 kcal)", "Lunch": "Grilled fish with rice (600 kcal)", "Dinner": "Chapati and dal (400 kcal)"},
                "Tuesday": {"Breakfast": "Oats and milk (300 kcal)", "Lunch": "Chicken curry with rice (600 kcal)", "Dinner": "Vegetable soup and bread (350 kcal)"},
                "Wednesday": {"Breakfast": "Poha (250 kcal)", "Lunch": "Paneer rice (550 kcal)", "Dinner": "Roti and sabzi (350 kcal)"},
                "Thursday": {"Breakfast": "Paratha and curd (300 kcal)", "Lunch": "Veg thali (550 kcal)", "Dinner": "Soup and salad (350 kcal)"},
                "Friday": {"Breakfast": "Milk and nuts (250 kcal)", "Lunch": "Grilled chicken with rice (600 kcal)", "Dinner": "Khichdi (350 kcal)"},
                "Saturday": {"Breakfast": "Idli sambar (250 kcal)", "Lunch": "Veg noodles (550 kcal)", "Dinner": "Dal and rice (350 kcal)"},
                "Sunday": {"Breakfast": "Smoothie bowl (300 kcal)", "Lunch": "Rajma rice (550 kcal)", "Dinner": "Egg curry and chapati (350 kcal)"}
            }
        },
        "50+": {
            "male": {
                "Monday": {"Breakfast": "Oats and milk (300 kcal)", "Lunch": "Dal rice (550 kcal)", "Dinner": "Vegetable soup (350 kcal)"},
                "Tuesday": {"Breakfast": "Upma (300 kcal)", "Lunch": "Grilled fish and rice (600 kcal)", "Dinner": "Khichdi (350 kcal)"},
                "Wednesday": {"Breakfast": "Poha (250 kcal)", "Lunch": "Paneer curry and rice (550 kcal)", "Dinner": "Chapati and dal (350 kcal)"},
                "Thursday": {"Breakfast": "Paratha and curd (300 kcal)", "Lunch": "Veg thali (550 kcal)", "Dinner": "Soup and salad (350 kcal)"},
                "Friday": {"Breakfast": "Milk and fruits (250 kcal)", "Lunch": "Chicken rice (600 kcal)", "Dinner": "Khichdi (350 kcal)"},
                "Saturday": {"Breakfast": "Idli sambar (250 kcal)", "Lunch": "Veg noodles (500 kcal)", "Dinner": "Roti and sabzi (350 kcal)"},
                "Sunday": {"Breakfast": "Smoothie bowl (300 kcal)", "Lunch": "Rajma rice (550 kcal)", "Dinner": "Dal soup (350 kcal)"}
            },
            "female": {
                "Monday": {"Breakfast": "Oats and milk (250 kcal)", "Lunch": "Dal rice (500 kcal)", "Dinner": "Vegetable soup (300 kcal)"},
                "Tuesday": {"Breakfast": "Upma (250 kcal)", "Lunch": "Grilled fish and rice (550 kcal)", "Dinner": "Khichdi (300 kcal)"},
                "Wednesday": {"Breakfast": "Poha (200 kcal)", "Lunch": "Paneer curry and rice (500 kcal)", "Dinner": "Chapati and dal (300 kcal)"},
                "Thursday": {"Breakfast": "Paratha and curd (250 kcal)", "Lunch": "Veg thali (500 kcal)", "Dinner": "Soup and salad (300 kcal)"},
                "Friday": {"Breakfast": "Milk and fruits (200 kcal)", "Lunch": "Chicken rice (550 kcal)", "Dinner": "Khichdi (300 kcal)"},
                "Saturday": {"Breakfast": "Idli sambar (200 kcal)", "Lunch": "Veg noodles (450 kcal)", "Dinner": "Roti and sabzi (300 kcal)"},
                "Sunday": {"Breakfast": "Smoothie bowl (250 kcal)", "Lunch": "Rajma rice (500 kcal)", "Dinner": "Dal soup (300 kcal)"}
            }
        }
    }

veg_replacements = {
        "chicken": "Paneer curry with rice (600 kcal)",
        "fish": "Tofu stir fry with rice (600 kcal)",
        "egg": "Moong dal chilla with salad (400 kcal)"
    }

# --- 1. CONFIGURATION ---
app = Flask(__name__)
CORS(app) # Crucial for website connectivity

# --- 3. DIET LOGIC (Modified function from your partner's script) ---

def get_diet_plan_logic(age, gender, preference, restrictions):
    # This function is derived from your partner's script, handles all logic.
    gender = gender.strip().lower()
    preference = preference.strip().lower()
    restrictions = [r.strip().lower() for r in restrictions]
    
    if 1 <= age < 13:
        group = "1-13"
    elif 13 <= age < 18:
        group = "13-18"
    elif 18 <= age < 35:
        group = "18-35"
    elif 35 <= age < 50:
        group = "35-50"
    else:
        group = "50+"

    if group not in diet_plans or gender not in diet_plans[group]:
        return {"error": "Plan not available for this group or gender."}

    # Deep copy plan to modify it safely
    plan = json.loads(json.dumps(diet_plans[group][gender])) 

    if preference == "veg":
        for day in plan:
            for meal in plan[day]:
                for nonveg_item, veg_alt in veg_replacements.items():
                    if nonveg_item in plan[day][meal].lower():
                       plan[day][meal] = veg_alt

    for day in plan:
        for meal in plan[day]:
            for restriction in restrictions:
                if restriction and restriction in plan[day][meal].lower():
                    plan[day][meal] = f"Alternative meal (no {restriction}) (400 kcal)"
    
    # Calculate and add total calories for the day (Holistic data)
    for day, meals in plan.items():
        total_calories = 0
        for item in meals.values():
            try:
                # Extracts the kcal value from the string
                kcal = int(item.split("(")[1].split()[0])
                total_calories += kcal
            except:
                pass
        plan[day]["total_calories"] = total_calories
    
    return plan


# --- 4. DIET API ENDPOINT ---

@app.route('/api/diet/plan', methods=['POST'])
def get_diet_plan_api():
    data = request.get_json()
    
    # Frontend must pass parameters needed by the logic
    age = data.get('age')
    gender = data.get('gender')
    preference = data.get('preference')
    restrictions = data.get('restrictions', [])
    
    if not all([age, gender, preference]):
        return jsonify({"error": "Missing age, gender, or preference."}), 400
        
    result = get_diet_plan_logic(age, gender, preference, restrictions)
    
    if "error" in result:
        return jsonify(result), 404
    else:
        return jsonify(result), 200


# --- 5. RUN THE APPLICATION ---
if __name__ == '__main__':
    # CRUCIAL: Run this on PORT 5001 to avoid conflict with your Workouts app (Port 5000)
    app.run(port=5001, debug=True)