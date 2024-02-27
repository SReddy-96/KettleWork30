from cs50 import SQL
import random
from flask import redirect, render_template, session
from functools import wraps

db = SQL("sqlite:///workouts.db")

def rand_workout(db_table, num_times):
    workouts = {}
    while len(workouts) < num_times:  # Fetch num_times random workouts
        rand = random.randint(1, 15)
        if rand not in workouts:
            # Assuming db.execute returns a dictionary or a list of dictionaries
            workout = db.execute(f"SELECT id, name, image_url, description FROM {db_table} WHERE id = ?", rand)
            if workout:  # Check if the workout is not empty
                workouts[rand] = workout[0]  # Assuming the query returns one workout
    return workouts

def apology(message, code=400):
		return render_template("apology.html", message=message, code=code)

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def repeat_exercise(warmup, exercise, cooldown):
    TOTAL_EXERCISES = 27
    TOTAL_WORKOUT = 30

    merged_dict = {}
    current_id = 1  # Start ID from 1

    # Assign numerical IDs for warm-up
    for i, (key, value) in enumerate(warmup.items(), start=current_id):
        merged_dict[i] = value
        current_id += 1

    # Assign numerical IDs for exercises
    while len(merged_dict) < TOTAL_EXERCISES:
        for i, (key, value) in enumerate(exercise.items(), start=current_id):
            if len(merged_dict) >= TOTAL_EXERCISES:
                break
            merged_dict[current_id] = value
            current_id += 1

    # Assign numerical IDs for cool-down
    for i, (key, value) in enumerate(cooldown.items(), start=current_id):
        if len(merged_dict) >= TOTAL_WORKOUT:
            break
        merged_dict[i] = value
        current_id += 1

    return merged_dict





