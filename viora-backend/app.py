from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate # <<< ADDED FOR MIGRATION
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import datetime
import os
import json
# --- 1. CONFIGURATION ---
basedir = os.path.abspath(os.path.dirname(__file__))

# CALCULATE PARENT DIRECTORY (To find 'templates' folder outside viora-backend)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# INITIALIZE FLASK WITH CORRECT FOLDER PATHS
app = Flask(__name__,
            static_folder=os.path.join(parent_dir, 'static'),
            template_folder=os.path.join(parent_dir, 'templates'))

CORS(app)
app.config['SECRET_KEY'] = 'a_secure_and_random_string_for_viora' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'viora.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# --- WORKOUT DATA (PHASE 3: Workout Plan Data) ---

WORKOUT_PLANS = {
    # 3-12 years: REMAINS AS ORIGINALLY PLANNED (Light Activity)
    "Child_Activity": {
        "focus": "Active Play, Coordination, and Motor Skills",
        "plan": [
            {"day": "Monday", "type": "Active Play", "activity": "Running/Tag", "duration_min": 60, "notes": "Focus on high-energy, sustained play."},
            {"day": "Wednesday", "type": "Skills", "activity": "Hopping/Jumping Games", "duration_min": 45, "notes": "Improves coordination and balance."},
            {"day": "Friday", "type": "Sport", "activity": "Swimming/Cycling", "duration_min": 60, "notes": "Introduces structured physical movement."},
        ]
    },

    # 13-18 years: CHANGED TO PUSH/PULL/LEGS (Bodyweight/Form Focus)
    "Teen_Development": {
        "focus": "Building Foundation and Form using Push/Pull/Legs Split",
        "plan": [
            {"day": "Monday", "type": "Push (Bodyweight/Light)", "exercises": ["Incline Push-ups (3x12)", "Dumbbell Overhead Press (3x10)", "Triceps Dips (3x10)"], "notes": "Focus on excellent form. No heavy weights."},
            {"day": "Tuesday", "type": "Pull (Bodyweight/Light)", "exercises": ["Inverted Rows (3x12)", "Band Pull-aparts (3x15)", "Hammer Curls (3x10)"], "notes": "Build postural strength."},
            {"day": "Wednesday", "type": "Legs (Bodyweight)", "exercises": ["Bodyweight Squats (3x20)", "Walking Lunges (3x10 each leg)", "Calf Raises (3x20)"], "notes": "High volume for strength endurance."},
            {"day": "Thursday", "type": "Rest/Active Recovery", "activity": "Light walk", "duration_min": 20, "notes": "Focus on recovery."},
            {"day": "Friday", "type": "Full Body Mixed", "activity": "Sport/HIIT", "duration_min": 45, "notes": "Engage in sports or light circuit training."},
        ]
    },

    # 18-35 years: CHANGED TO PUSH/PULL/LEGS (Strength/Hypertrophy Focus)
    "Adult_Standard": {
        "focus": "Maximum Strength and Muscle Hypertrophy using Push/Pull/Legs Split",
        "plan": [
            {"day": "Monday", "type": "Push (Heavy)", "exercises": ["Barbell Bench Press (3x5)", "Overhead Press (3x8)", "Lateral Raises (3x12)", "Triceps Extensions (3x10)"], "notes": "Heavy compound lifts. Manage intensity."},
            {"day": "Tuesday", "type": "Pull (Heavy)", "exercises": ["Deadlifts (3x5)", "Barbell Rows (3x8)", "Lat Pulldowns (3x10)", "Bicep Curls (3x12)"], "notes": "Focus on back thickness and width."},
            {"day": "Wednesday", "type": "Legs (Heavy)", "exercises": ["Barbell Squats (3x8)", "Leg Press (3x10)", "Hamstring Curls (3x10)"], "notes": "Prioritize progressive overload."},
            {"day": "Thursday", "type": "Rest/Cardio", "activity": "Jogging/Cycling", "duration_min": 30, "notes": "Low-impact active recovery."},
            {"day": "Friday", "type": "PPL Repeat (Optional)", "activity": "Push/Pull/Legs day 4", "notes": "Allows for higher training frequency."},
        ]
    },

    # 35-50 years: REMAINS AS ORIGINALLY PLANNED (Light Weights, Joint-Friendly)
    "Middle_Age_Light": {
        "focus": "Joint Stability, Cardiovascular Health, and Functional Movement",
        "plan": [
            {"day": "Monday", "type": "Resistance (Light Weights)", "exercises": ["Leg Press (3x15, slow tempo)", "Cable Rows (3x15)", "Light Dumbbell Bench Press"], "notes": "Focus on controlled movements and higher repetitions."},
            {"day": "Wednesday", "type": "Low-Impact Cardio", "activity": "Cycling/Elliptical", "duration_min": 45, "notes": "Maintain target heart rate without high impact."},
            {"day": "Friday", "type": "Flexibility/Core", "activity": "Pilates/Advanced Stretching", "duration_min": 30, "notes": "Improves posture and core strength."},
        ]
    },

    # 50+ years: REMAINS AS ORIGINALLY PLANNED (Mobility/Balance Focus)
    "Senior_Light": {
        "focus": "Balance, Flexibility, and Mobility (No Heavy Weights)",
        "plan": [
            {"day": "Monday", "type": "Functional Movement", "exercises": ["Chair Squats (3x10)", "Wall Push-ups (3x10)"], "notes": "Focus on standing/sitting ability. Use support if needed."},
            {"day": "Wednesday", "type": "Cardio", "activity": "Brisk Walking", "distance_km": 2, "notes": "Focus on consistent pace. Monitor comfort level."},
            {"day": "Friday", "type": "Balance/Stretch", "activity": "Yoga/Tai Chi", "duration_min": 20, "notes": "Improves stability to prevent falls."},
        ]
    },
}
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



# --- 2. HELPER FUNCTIONS ---

# Function to calculate age from date of birth object
def calculate_age(dob):
    today = datetime.date.today()
    if dob is None:
        return 0 
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

# Function to assign the workout category based on your project requirements
def get_age_category(age):
    if 3 <= age <= 12:
        return "Child_Activity"
    elif 13 <= age <= 18:
        return "Teen_Development"
    elif 19 <= age <= 35:
        return "Adult_Standard"
    elif 36 <= age <= 50:
        return "Middle_Age_Light"
    elif age >= 51:
        return "Senior_Light"
    else:
        return "Not_Categorized"
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


# --- 3. DATA MODELS ---

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # <<< NEWLY ADDED NAME FIELD >>>
    name = db.Column(db.String(100), nullable=False) 
    
    username = db.Column(db.String(80), unique=True, nullable=False) # Login ID
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    date_of_birth = db.Column(db.Date) # Age is derived from this
    
    # <<< NEWLY ADDED METRICS >>>
    height_cm = db.Column(db.Integer)
    weight_kg = db.Column(db.Float)
    
    workouts = db.relationship('Workout', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# --- INSERT THESE TWO NEW CLASSES HERE (Around line 140) ---

class Workout(db.Model):
    # This now represents the start/end of a workout SESSION
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    end_time = db.Column(db.DateTime)
    
    # Relationship to the details table (ExerciseLog)
    exercises = db.relationship('ExerciseLog', backref='workout', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            # Total duration/volume will be calculated in the API route, not stored here
        }

class ExerciseLog(db.Model):
    # This stores every single set logged by the user, including custom ones
    id = db.Column(db.Integer, primary_key=True)
    
    # Link back to the main workout session
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    
    # 1. User-Added Workout Feature: The user types this name
    exercise_name = db.Column(db.String(100), nullable=False) 
    
    # 2. Template/Set Tracking: Detailed fields for each set
    set_number = db.Column(db.Integer, nullable=False)
    weight_kg = db.Column(db.Float, default=0.0) 
    reps = db.Column(db.Integer, default=0)
    
    # For bodyweight/time-based exercises like Plank
    duration_seconds = db.Column(db.Integer, default=0)
# -------------------------------------------------------------------
# --- END OF MODELS ---

# --- 4. CORE API ROUTES ---

@app.route('/api/register', methods=['POST'])
def register():
    """Registers a new user with all profile metrics."""
    data = request.get_json()
    username = data.get('username') 
    name = data.get('name')         # <<< GETS NEW NAME
    email = data.get('email')
    password = data.get('password')
    dob_str = data.get('date_of_birth')
    height = data.get('height_cm')  # <<< GETS NEW HEIGHT
    weight = data.get('weight_kg')  # <<< GETS NEW WEIGHT
    
    # Validation for all new fields
    if not all([username, name, email, password, dob_str, height, weight]):
        return jsonify({"message": "Missing all required fields (username, name, email, password, date_of_birth, height_cm, weight_kg)"}), 400

    try:
        dob = datetime.datetime.strptime(dob_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"message": "Invalid date format. Use YYYY-MM-DD"}), 400

    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        return jsonify({"message": "Email or Username already registered"}), 409

    # Create user with all new fields
    new_user = User(
        username=username, 
        name=name,           # <<< SAVES NEW NAME
        email=email, 
        date_of_birth=dob,
        height_cm=height,    # <<< SAVES NEW HEIGHT
        weight_kg=weight     # <<< SAVES NEW WEIGHT
    )
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": f"User {name} successfully registered! Age: {calculate_age(dob)}", "user_id": new_user.id}), 201

@app.route('/api/login', methods=['POST'])
def login():
    """Logs in a user and returns their full profile data."""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()

    # Securely checks password
    if user is None or not user.check_password(password):
        return jsonify({"message": "Invalid email or password"}), 401

    # <<< RETURNS ALL NEW PROFILE DATA >>>
    return jsonify({
        "message": "Login successful!",
        "user_id": user.id,
        "username": user.username, 
        "name": user.name,         
        "height_cm": user.height_cm, 
        "weight_kg": user.weight_kg, 
        "age": calculate_age(user.date_of_birth) # Returns calculated age
    }), 200 
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
# --- 6. USER PROFILE UPDATE ROUTE ---
@app.route('/api/user/update_profile/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    """Updates an existing user's profile data (height, weight, etc.)."""
    
    # Find the user in the database
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()

    # Get new data from the request, but keep the old data if nothing new is provided
    user.name = data.get('name', user.name)
    user.height_cm = data.get('height_cm', user.height_cm)
    user.weight_kg = data.get('weight_kg', user.weight_kg)
    
    # You could also allow username or email changes here, but it's more complex
    # For example: user.username = data.get('username', user.username)

    try:
        db.session.commit()
        # Return the newly updated profile
        return jsonify({
            "message": "Profile updated successfully!",
            "user_id": user.id,
            "name": user.name,
            "height_cm": user.height_cm,
            "weight_kg": user.weight_kg
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update profile", "details": str(e)}), 500
    
# --- 7. SYNC ROUTE FOR DIET MODULE ---
@app.route('/api/workouts/is_active_day/<int:user_id>', methods=['GET'])
def is_active_day(user_id):
    """Checks if the user logged a workout today (for the Diet module to call)."""
    
    # Get today's date
    today = datetime.datetime.utcnow().date()
    
    # Check if a workout session exists in the database for this user on this date
    active_session_today = Workout.query.filter(
        Workout.user_id == user_id,
        db.func.date(Workout.start_time) == today 
    ).first()
    
    # Return True if a session was found, False otherwise
    if active_session_today:
        return jsonify({"user_id": user_id, "is_active": True, "message": "High activity detected today."}), 200
    else:
        return jsonify({"user_id": user_id, "is_active": False, "message": "Low activity detected today."}), 200

# --- PASTE THIS NEW ROUTE HERE (Where the old 'add_workout' was) ---

@app.route('/api/workout/log_session', methods=['POST'])
def log_full_workout_session():
    """Logs a complete workout session with multiple exercises and sets."""
    data = request.get_json()
    user_id = data.get('user_id')
    exercises_data = data.get('exercises') 

    if not user_id or not exercises_data:
        return jsonify({"error": "Missing user_id or exercise data"}), 400

    try:
        # 1. Create the main Workout Session record (WITHOUT end_time)
        new_session = Workout(
            user_id=user_id,
            start_time=datetime.datetime.utcnow() 
        )
        db.session.add(new_session)
        db.session.flush() # Get the new_session.id before committing

        # 2. Loop through exercises and log every single set
        total_sets = 0
        for exercise in exercises_data:
            exercise_name = exercise.get('name', 'Custom Exercise') 
            for set_data in exercise.get('sets', []):
                new_log = ExerciseLog(
                    workout_id=new_session.id,
                    exercise_name=exercise_name,
                    set_number=set_data.get('set_number', 1),
                    weight_kg=set_data.get('weight_kg', 0.0),
                    reps=set_data.get('reps', 0),
                    duration_seconds=set_data.get('duration_seconds', 0)
                )
                db.session.add(new_log)
                total_sets += 1
        
        # <<< FIX: Set end_time AFTER loops are done >>>
        new_session.end_time = datetime.datetime.utcnow()
        
        db.session.commit() # Saves everything at once

        return jsonify({
            "message": "Full workout logged successfully!",
            "session_id": new_session.id,
            "total_exercises_logged": len(exercises_data),
            "total_sets_logged": total_sets
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to log workout details", "details": str(e)}), 400
# -------------------------------------------------------------------
@app.route('/api/workout_plan/<int:user_id>', methods=['GET'])
def get_personalized_plan(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404

    # 1. Get Age from DOB
    age = calculate_age(user.date_of_birth)
    
    # 2. Determine Category
    category = get_age_category(age)
    
    # 3. Fetch the Plan from the dictionary
    plan_data = WORKOUT_PLANS.get(category)
    
    if plan_data is None:
         return jsonify({"message": "Plan not available (Age not set or not categorized)"}), 404
    
    # 4. Return the Plan
    return jsonify({
        "user_id": user_id,
        "age": age,
        "category": category,
        "plan": plan_data
    }), 200
# --- FRONTEND PAGE ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/workout')
def workout():
    return render_template('workout.html')

@app.route('/diet')
def diet():
    return render_template('diet.html') 

# --- 5. RUN THE APPLICATION ---

if __name__ == '__main__':
    app.run(port=5000, debug=True)
