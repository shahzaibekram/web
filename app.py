from flask import Flask, render_template, request, flash, redirect, jsonify
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from pony.flask import Pony
from datetime import date
import time
from pony.orm import *
from werkzeug.security import generate_password_hash, check_password_hash
import json

app = Flask(__name__)
app.config.update(dict(
    DEBUG=False,
    SECRET_KEY='secret_xxxmoiracekadaxxx',
    PONY={
        'provider': 'sqlite',
        'filename': 'event_planner.db',
        'create_db': True
    }
))

db = Database()


class Organizer(db.Entity, UserMixin):
    id = PrimaryKey(int, auto=True)
    name = Required(str, 40)
    email = Required(str, unique=True)
    password = Required(str)
    phone = Required(str)
    events = Set("Event")


class Event(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    description = Required(str)
    date = Required(date)
    time = Required(str, default=str(time.time()))
    location = Required(str)
    organizer = Required(Organizer, column="user_id")


db.bind(**app.config['PONY'])
db.generate_mapping(create_tables=True)

Pony(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index.html"


@login_manager.user_loader
def load_user(user_id):
    return Organizer.get(id=user_id)


@app.route("/")
# @login_required
def home():
    return render_template('index.html', user=current_user)


@app.route("/about")
# @login_required
def about():
    return render_template('about.html', user=current_user)


@app.route("/events", methods=['GET', 'POST'])
def events():

    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        date = request.form.get('date')
        time = request.form.get('time')
        messageText = request.form.get('messageText')

        # if len(name) < 3:
        #     flash("Please enter a valid Event name.", category="error")
        # if len(messageText) < 5:
        #     flash("Please enter a valid Event description.", category="error")
        # else:
        with db_session:
            new_event = Event(name=name, location=location,
                              date=date, time=time, description=messageText, organizer=current_user.id)
        flash("Event created!", category="success")

    return render_template('events.html', user=current_user)


@app.route("/delete-event", methods=['POST'])
def delete_event():
    with db_session:
        event = json.loads(request.data)
        eventId = event["eventId"]
        event = Event.get(id=eventId)
        event.delete()
        flash("The event deleted.", category="success")

    return render_template('events.html', user=current_user)


@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user_email = Organizer.get(email=email)
        if user_email:
            if check_password_hash(user_email.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user_email, remember=True)
                return redirect("/")
            else:
                flash("Incorrect password! Try again.", category="error")
        else:
            flash("Email doesn't exist.", category="error")

        if len(email) < 10:
            flash("Please enter a valid email.", category="error")
        elif ".com" not in email:
            flash("Please enter a valid email.", category="error")
        elif len(password) < 6:
            flash("Password must be at least 6 characters", category="error")

    return render_template('login.html', user=current_user)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('index.html', user=current_user)


@app.route("/signup", methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user_email = Organizer.get(email=email)
        if user_email:
            flash(
                "A user with this email already exists. Try again with another email.", category="error")
        elif len(name) < 3:
            flash("Name must be at least 3 characters.", category="error")
        elif len(email) < 10:
            flash("Email must be at least 10 characters.", category="error")
        elif ".com" not in email:
            flash("Email must contain .com at the end.", category="error")
        elif password1 != password2:
            flash("Your password doesn\'t match.", category="error")
        elif len(password1) < 6:
            flash("Password must be at least 6 characters", category="error")
        else:
            new_user = Organizer(email=email, name=name, phone=phone,
                                 password=generate_password_hash(password1, method="sha256"))
            commit()
            flash("Account created successfully. Please, Log in to access.",
                  category="success")
            return redirect("/login")

    return render_template('signup.html', user=current_user)


if __name__ == "__main__":
    app.run(debug=True)
