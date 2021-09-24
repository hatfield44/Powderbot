from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from .models import Location, User
from website import db
from sqlalchemy import func


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                # Loads the user's favorites or ''None' until selected
                favForecast1 = Location.query.filter_by(name=current_user.fav1).scalar()
                favForecast2 = Location.query.filter_by(name=current_user.fav2).scalar()
                favForecast3 = Location.query.filter_by(name=current_user.fav3).scalar()
                favForecast4 = Location.query.filter_by(name=current_user.fav4).scalar()
                # If there are multiple location with the same forecasted amount
                # the deepest location will be the first one in the list
                # Gets the deepest locations for each pass.
                # Get maximum depth forecasted for ikon
                deepestIkon = db.session.query(func.max(Location.forecast0)).filter(Location.ikon == 1).scalar()
                # Get the first of the locations that has the maximum depth as the days forecast for ikon if multiples
                deepIkon = Location.query.filter_by(forecast0 = deepestIkon).filter(Location.ikon == 1).all()[0]
                # Get maximum depth forecasted for epic
                deepestEpic = db.session.query(func.max(Location.forecast0)).filter(Location.epic == 1).scalar()
                # Get the first of the locations that has the maximum depth as the days forecast for epic if multiples
                deepEpic = Location.query.filter_by(forecast0 = deepestEpic).filter(Location.epic == 1).all()[0]
                # Get maximum depth forecasted for mountain collective
                deepestMC = db.session.query(func.max(Location.forecast0)).filter(Location.mc == 1).scalar()
                # Get the first of the locations that has the maximum depth as the days forecast for mountain collective if multiples
                deepMC = Location.query.filter_by(forecast0 = deepestMC).filter(Location.mc == 1).all()[0]
                # Get maximum depth forecasted for powder alliance
                deepestPowder = db.session.query(func.max(Location.forecast0)).filter(Location.powder == 1).scalar()
                # Get the first of the locations that has the maximum depth as the days forecast for powder alliance if multiples
                deepPowder = Location.query.filter_by(forecast0 = deepestPowder).filter(Location.powder == 1).all()[0]
                # Get maximum depth forecasted for indy
                deepestIndy = db.session.query(func.max(Location.forecast0)).filter(Location.indy == 1).scalar()
                # Get the first of the locations that has the maximum depth as the days forecast for indy if multiples
                deepIndy = Location.query.filter_by(forecast0 = deepestIndy).filter(Location.indy == 1).all()[0]
                return render_template("favorites.html", boolean=True, favorite1 = favForecast1, favorite2 = favForecast2, favorite3 = favForecast3, favorite4 = favForecast4, deepIkon = deepIkon, deepEpic = deepEpic, deepMC = deepMC, deepPowder = deepPowder, deepIndy = deepIndy)
            else:
                flash('Email or Password not recognized!', category = 'error')
        else:
            flash('Email or Password not recognized!', category = 'error')
    return render_template("login.html")

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have logged out.', category='success')
    return redirect(url_for('views.home'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    # Get form info to check and add user to db
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        # Check for previous registration
        user = User.query.filter_by(email = email).first()
        # Check user input for validity
        if user:
            flash('Email already registered', category = 'error')
        elif (len(email) < 4):
            flash('Please enter a valid email', category = 'error')
        elif (len(password1) < 8):
            flash("Password must be at least 8 characters", category = 'error')
        elif (password1 != password2):
            flash('Passwords do not match.', category = 'error')
        else:
            # create a new user with form info
            new_user = User(email=email, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user) # add the user to the db
            db.session.commit() # commit changes to db
            login_user(new_user, remember = True) # Log new user in 
            flash('Account created!', category='success')
            return redirect(url_for('views.setfavorites'))
    
    return render_template("register.html")

