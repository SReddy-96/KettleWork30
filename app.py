import os
from cs50 import SQL
import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api 
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import json
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, rand_workout, repeat_exercise

#load .env
#load_dotenv()

# Set configuration parameter: return "https" URLs by setting secure=True  
#cloudinary.config(secure=True, cloud_url=os.getenv(CLOUDINARY_URL))

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///workouts.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/workout", methods=["GET","POST"])
@login_required
def workout():
        #post request
    if request.method == 'POST':
        # results from the form
        level = request.form.get('level-outlined')
        exercise = request.form.get('exercise-outlined')

        # define warmup and cooldown
        warmup = rand_workout("warmup", 3)
        if not warmup:
	        return apology("warmup DB fail", 400)

        cooldown = rand_workout("cooldown", 3)
        if not cooldown:
	        return apology("cooldown DB fail", 400)

        # using the results form form to create the workout.
        if level == "easy" and exercise == "push":	
            pusheasyworkout = repeat_exercise(warmup, (rand_workout("pusheasy", 8)), cooldown)
            if not pusheasyworkout:		
                return apology("Workout error", 400)	
            names = ', '.join(value['name'] for value in pusheasyworkout.values()) 
            db.execute("INSERT INTO history (user_id, level, names) VALUES (?, ?, ?)", session["user_id"], "easy", names)
            return render_template("active.html", workout=pusheasyworkout)

        if level == "easy" and exercise == "pull":
            pulleasy = rand_workout("pulleasy", 8)
            pulleasyworkout = repeat_exercise(warmup, pulleasy, cooldown)
            if not pulleasyworkout:		
                return apology("Workout error", 400)	
            names = ', '.join(value['name'] for value in pulleasyworkout.values())   
            db.execute("INSERT INTO history (user_id, level, names) VALUES (?, ?, ?)", session["user_id"], "easy", names)    
            return render_template("active.html", workout=pulleasyworkout)

        if level == "easy" and exercise == "leg":
            legeasy = rand_workout("legeasy", 8)
            legeasyworkout = repeat_exercise(warmup, legeasy, cooldown)
            if not legeasyworkout:		
                return apology("Workout error", 400)	
            names = ', '.join(value['name'] for value in legeasyworkout.values())   
            db.execute("INSERT INTO history (user_id, level, names) VALUES (?, ?, ?)", session["user_id"], "easy", names)    
            return render_template("active.html", workout=legeasyworkout)
        
        if level == "medium" and exercise == "pull":
            pullmed = rand_workout("pullmed", 8)
            pullmedworkout = repeat_exercise(warmup, pullmed, cooldown)
            if not pullmedworkout:		
                return apology("Workout error", 400)	
            names = ', '.join(value['name'] for value in pullmedworkout.values())   
            db.execute("INSERT INTO history (user_id, level, names) VALUES (?, ?, ?)", session["user_id"], "medium", names)    
            return render_template("active.html", workout=pullmedworkout)

        if level == "medium" and exercise == "push":
            pushmed = rand_workout("pushmed", 8)
            pushmedworkout = repeat_exercise(warmup, pushmed, cooldown)
            if not pushmedworkout:		
                return apology("Workout error", 400)	
            names = ', '.join(value['name'] for value in pushmedworkout.values())   
            db.execute("INSERT INTO history (user_id, level, names) VALUES (?, ?, ?)", session["user_id"], "medium", names)    
            return render_template("active.html", workout=pushmedworkout)
        
        if level == "medium" and exercise == "leg":
            legmed = rand_workout("legmed", 8)
            legmedworkout = repeat_exercise(warmup, legmed, cooldown)
            if not legmedworkout:		
                return apology("Workout error", 400)	
            names = ', '.join(value['name'] for value in legmedworkout.values())   
            db.execute("INSERT INTO history (user_id, level, names) VALUES (?, ?, ?)", session["user_id"], "medium", names)    
            return render_template("active.html", workout=legmedworkout)
        
        if level == "hard" and exercise == "push":
            pushhard = rand_workout("pushhard", 8)
            pushhardworkout = repeat_exercise(warmup, pushhard, cooldown)
            if not pushhardworkout:		
                return apology("Workout error", 400)	
            names = ', '.join(value['name'] for value in pushhardworkout.values())   
            db.execute("INSERT INTO history (user_id, level, names) VALUES (?, ?, ?)", session["user_id"], "hard", names)    
            return render_template("active.html", workout=pushhardworkout)
        
        if level == "hard" and exercise == "pull":
            pullhard = rand_workout("pullhard", 8)
            pullhardworkout = repeat_exercise(warmup, pullhard, cooldown)
            if not pullhardworkout:		
                return apology("Workout error", 400)	
            names = ', '.join(value['name'] for value in pullhardworkout.values())   
            db.execute("INSERT INTO history (user_id, level, names) VALUES (?, ?, ?)", session["user_id"], "hard", names)    
            return render_template("active.html", workout=pullhardworkout)

        if level == "hard" and exercise == "leg":
            leghard = rand_workout("leghard", 8)
            leghardworkout = repeat_exercise(warmup, leghard, cooldown)
            if not leghardworkout:		
                return apology("Workout error", 400)	
            names = ', '.join(value['name'] for value in leghardworkout.values())   
            db.execute("INSERT INTO history (user_id, level, names) VALUES (?, ?, ?)", session["user_id"], "hard", names)    
            return render_template("active.html", workout=leghardworkout)
        
        if level == "easy" and exercise == "fullbody":
            rand1easy = rand_workout("pusheasy", 3)
            rand2easy = rand_workout("pulleasy", 3)
            rand3easy = rand_workout("legeasy", 2)
            
            #to change the id so nothing clashes when merging
            rand2easy = {k + 1000: v for k, v in rand2easy.items()}
            rand3easy = {k + 2000: v for k, v in rand3easy.items()}
            fullbodyeasy = {**rand1easy, **rand2easy, **rand3easy}
            fullbodyeasyworkout = repeat_exercise(warmup, fullbodyeasy, cooldown)
            if not fullbodyeasyworkout:		
                return apology("Workout error", 400)	
            names = ', '.join(value['name'] for value in fullbodyeasyworkout.values())   
            db.execute("INSERT INTO history (user_id, level, names) VALUES (?, ?, ?)", session["user_id"], "easy", names)    
            return render_template("active.html", workout=fullbodyeasyworkout)
        
        if level == "medium" and exercise == "fullbody":
            rand1med = rand_workout("pushmed", 3)
            rand2med = rand_workout("pullmed", 3)
            rand3med = rand_workout("legmed", 2)
            
            #to change the id so nothing clashes when merging
            rand2med = {k + 1000: v for k, v in rand2med.items()}
            rand3med = {k + 2000: v for k, v in rand3med.items()}
            fullbodymed = {**rand1med, **rand2med, **rand3med}
            fullbodymedworkout = repeat_exercise(warmup, fullbodymed, cooldown)
            if not fullbodymedworkout:		
                return apology("Workout error", 400)	
            names = ', '.join(value['name'] for value in fullbodymedworkout.values())   
            db.execute("INSERT INTO history (user_id, level, names) VALUES (?, ?, ?)", session["user_id"], "medium", names)    
            return render_template("active.html", workout=fullbodymedworkout)

        if level == "hard" and exercise == "fullbody":
            rand1hard = rand_workout("pushhard", 3)
            rand2hard = rand_workout("pullhard", 3)
            rand3hard = rand_workout("leghard", 2)
            
            #to change the id so nothing clashes when merging
            rand2hard = {k + 1000: v for k, v in rand2hard.items()}
            rand3hard = {k + 2000: v for k, v in rand3hard.items()}
            fullbodyhard = {**rand1hard, **rand2hard, **rand3hard}
            fullbodyhardworkout = repeat_exercise(warmup, fullbodyhard, cooldown)
            print(fullbodyhardworkout)
            if not fullbodyhardworkout:
                return apology("Workout error", 400)	
            names = ', '.join(value['name'] for value in fullbodyhardworkout.values())
            fullbodyhardworkout = json.dumps(fullbodyhardworkout)
            db.execute("INSERT INTO history (user_id, level, names) VALUES (?, ?, ?)", session["user_id"], "hard", names)    
            return render_template("active.html", workout=fullbodyhardworkout)
        
        return apology("no valid response", 400)
    #get request
    else:
        return render_template("workout.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return apology("enter a Username", 400)

        username_check = db.execute("SELECT * FROM users WHERE username = ?", username)
        if username_check:
            return apology("username already excists", 400)

        password = request.form.get("password")
        if not password:
            return apology("enter a password", 400)

        confirmation = request.form.get("confirmation")
        if password != confirmation:
            return apology("passwords do not match", 400)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))
        return redirect("/")

    # get request
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
@app.route("/history")
@login_required
def history():
    #Show history of transactions
    histories = []
    workouts = db.execute("SELECT * FROM history WHERE user_id = ?", session["user_id"])
    if not workouts:
        return apology("no portfolio", 400)

    for workout in workouts:
        # Create a new dictionary for each portfolio
        each_workout = {}
        each_workout["level"] = workout["level"]
        each_workout["names"] = workout["names"]
        each_workout["Timestamp"] = workout["Timestamp"]


        # Append the dictionary to the list
        histories.append(workout)

    return render_template("history.html", histories=histories)