from flask import Blueprint, render_template, request, url_for, flash, redirect, session
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from .models import Location, User
from website import db
from sqlalchemy import func, desc, text

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    # If there are multiple location with the same forecasted amount
    # the deepest location will be the first one in the list
    # Gets the location that has the deepest forecast for the day
    maxSnow = db.session.query(func.max(Location.forecast0)).scalar()
    # Get the first of the locations that has the maximum depth as the days forecast if multiples
    deepest = Location.query.filter_by(forecast0 = maxSnow).all()[0]
    
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

    # Lets user select a location to see the forecast    
    locations = Location.query.all() # Stores all locations in array
    chosenLocal = request.form.get('chosen') # Gets the selection from the user
    chosen = Location.query.filter_by(name=chosenLocal).scalar() # Gets the forecast for the chosec location

    return render_template("home.html", user=current_user, deepest = deepest, locations=locations, chosenLocal = chosen, deepIkon = deepIkon, deepEpic = deepEpic, deepMC = deepMC, deepPowder = deepPowder, deepIndy = deepIndy)

@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    searchStyles = ["Pass", "Reigon", "State"]  # Ways to search
    passes = ["Ikon", "Epic", "Mountain Collective", "Powder Alliance", "Indy"] # Passes to search
    if request.method == 'POST':
        searchStyle = "/search" + request.form.get('style') # Creates the path for the redirect from users chosen style
        session['searchStyle'] = request.form.get('style') # Session variable to carry selected search through redirect
        return redirect(searchStyle) # Redirects to the appropriate page for selected search
    else:
        # Return the page to allow the user to select style to search
        return render_template("search.html", user=current_user, searchStyles = searchStyles)

@views.route('/searchPass', methods=['GET', 'POST'])
@login_required
def searchPass():
    passes = ["Ikon", "Epic", "Mountain Collective", "Powder Alliance", "Indy"] # Passes to search
    if request.method == 'POST':
        session['searchParamater'] = request.form.get('selectedPass') # Session variable to carry selected pass through redirect
        return redirect('/searchResults')
    else:
        # Return the page to allow the user to select pass
        return render_template("searchPass.html", passes = passes)

@views.route('/searchState', methods=['GET', 'POST'])
@login_required
def searchState():
    # states to search by
    states = ["AK", "AZ", "CA", "CO", "CT", "ID", "IL", "IN", "MA", "MD", "ME", "MI", "MN", "MO", "MT", "NC", "ND", "NH", "NJ", "NM", "NV", "NY", "OH", "OR", "PA", "RI", "SD", "TN", "UT", "VA", "VT", "WA", "WI", "WV", "WY"]
    if request.method == 'POST':
        session['searchParamater'] = request.form.get('selectedState') # Session variable to carry selected pass through redirect
        return redirect('/searchResults')
    else:
        # Return the page to allow the user to select state
        return render_template("searchState.html", states = states)

@views.route('/searchReigon', methods=['GET', 'POST'])
@login_required
def searchReigon():
    # reigons to search by
    reigons = ["MidWest", "NorthEast", "Rockies", "SouthEast", "West"]
    if request.method == 'POST':
        session['searchParamater'] = request.form.get('selectedReigon') # Session variable to carry selected pass through redirect
        return redirect('/searchResults')
    else:
        # Return the page to allow the user to select reigon
        return render_template("searchReigon.html", reigons = reigons)

@views.route('/searchResults')
@login_required
def searchResults():
    # Gets the 4 deepest locations filtered by searchStyle
    # Get search by pass Pass results
    if (session['searchStyle'] == 'Pass'):
        searchParamater = session['searchParamater']
        if searchParamater == 'Ikon':
            query = Location.query.filter(Location.ikon == 1).order_by(desc(Location.forecast0)).all()[0:4]
        elif searchParamater == 'Epic':
            query = Location.query.filter(Location.epic == 1).order_by(desc(Location.forecast0)).all()[0:4]
        elif searchParamater == 'Mountain Collective':
            query = Location.query.filter(Location.mc == 1).order_by(desc(Location.forecast0)).all()[0:4]
        elif searchParamater == 'Powder Alliance':
            query = Location.query.filter(Location.powder == 1).order_by(desc(Location.forecast0)).all()[0:4]
        elif searchParamater == 'Indy':
            query = Location.query.filter(Location.indy == 1).order_by(desc(Location.forecast0)).all()[0:4]
        return render_template("searchResults.html", query = query, searchParamater = searchParamater)
    # Get search by Reigon reuslts
    if(session['searchStyle'] == 'Reigon'):
        searchParamater = ""
        searchParamater = session['searchParamater']
        query = Location.query.filter(Location.reigon == searchParamater).order_by(desc(Location.forecast0)).all()[0:4]
        return render_template("searchResults.html", query = query, searchParamater = searchParamater)
    # Get search by State results
    if(session['searchStyle'] == 'State'):
        searchParamater = ""
        searchParamater = session['searchParamater']
        query = Location.query.filter(Location.state == searchParamater).order_by(desc(Location.forecast0)).all()[0:4]
        return render_template("searchResults.html", query = query, searchParamater = searchParamater)



@views.route('/favorites')
@login_required
def favorites():
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
    
    # Gets the forecast for the users 4 selected favorites
    favForecast1 = Location.query.filter_by(name=current_user.fav1).scalar()
    favForecast2 = Location.query.filter_by(name=current_user.fav2).scalar()
    favForecast3 = Location.query.filter_by(name=current_user.fav3).scalar()
    favForecast4 = Location.query.filter_by(name=current_user.fav4).scalar()

    return render_template("favorites.html", favorite1 = favForecast1, favorite2 = favForecast2, favorite3 = favForecast3, favorite4 = favForecast4, deepIkon = deepIkon, deepEpic = deepEpic, deepMC = deepMC, deepPowder = deepPowder, deepIndy = deepIndy)


@views.route('/setfavorites', methods=['GET', 'POST'])
@login_required
def setfavorites():  # sourcery skip: list-comprehension, none-compare
    locals = [] # Holds all of the locations/resorts
    locations = Location.query.all() # Query results as a Tuple
    # For loop that appends query resutls from Tuple into the locals list
    for location in locations:
        locals.append(location.name)
    # Gets users pass information from form 
    if request.method == 'POST':
        if request.form.get('ikon') == None:
            current_user.ikon = 0
        else:
            current_user.ikon = request.form.get('ikon')
        if request.form.get('epic') == None:
            current_user.epic = 0
        else:
            current_user.epic = request.form.get('epic')
        if request.form.get('mc') == None:
            current_user.mc = 0
        else:
            current_user.mc = request.form.get('mc')
        if request.form.get('powder') == None:
            current_user.powder = 0
        else:
            current_user.powder = request.form.get('powder')
        if request.form.get('indy') == None:
            current_user.indy = 0
        else:
            current_user.indy = request.form.get('indy')

        # Gets users favorites from form
        current_user.fav1 = request.form.get('fav1')
        current_user.fav2 = request.form.get('fav2')
        current_user.fav3 = request.form.get('fav3')
        current_user.fav4 = request.form.get('fav4')

        db.session.commit() # Commits user pass/favorite information from form to db
        flash('Favorites Set!', category='success')
        return redirect("/favorites")

    return render_template("setfavorites.html", user=current_user, locations=locations)
