#!/usr/bin/env python3

import datetime
from google.oauth2 import id_token
from google.auth.transport import requests
from flask import Flask, render_template, request, make_response, redirect, url_for, session
from python.database.db import Database
from python.web.parking import get_parking_availability
from urllib.parse import parse_qs

app = Flask(__name__)
app.secret_key = 'uCraR5MZB/AvVo3Q24cBM/fZo5Kv/hV2HW9y0b3puClB25h0lbjBP6vYsHzz1hVY'
HOST, PORT = 'localhost', 8080
global userId, profile, buildings, favorites, classes, alerts, db
userId = None
profile = None
favorites = None
classes = None
alerts = None
db = Database()
buildings = db.get_all_buildings()

@app.route('/')
def index_page():
    global userId
    if  isValidSession(userId):
        return redirect(url_for('home_page'))
    return redirect(url_for('login_page'))
    
@app.route('/login')
def login_page():
    global userId
    if isValidSession(userId):
        return redirect(url_for('home_page'))
    return render_template('login.html', backDisplay=False, aboutDisplay=False, settingsDisplay=True, logDisplay=True)
    
@app.route('/logout')
def logout_page():
    global userId, profile, favorites, classes, alerts
    userId = None
    profile = None
    favorites = None
    classes = None
    alerts = None
    session.pop('user_id', None)
    return redirect(url_for('login_page'))
    
@app.route('/about')
def about_page():
    global userId
    if isValidSession(userId):
        return render_template('about.html', backDisplay=True, aboutDisplay=False)
    return redirect(url_for('login_page'))

@app.route('/profile', methods=['GET', 'POST'])
def profile_page():
    global userId, profile
    if isValidSession(userId):
        if request.method == 'GET':
            return render_template('profile.html', backDisplay=True, aboutDisplay=False)
        else:
            print("saving user settings")

            # profile.rec = request.form['rec']
            # profile.comType = request.form['comType']
            # db.update_profile(profile)
            
    return redirect(url_for('login_page'))

@app.route('/home')
def home_page():
    global userId, profile
    if isValidSession(userId):
        if profile == None:
            print("Retrieving user profile")
            # profile = db.get_profile_by_id(userId)
        return render_template('home.html', profileData=profile, backDisplay=False, aboutDisplay=True)
    return redirect(url_for('login_page'))
    
@app.route('/home', methods=['POST'])
def home_with_credentials_page():
    global userId, profile
    
    try:
        token = request.form['g_csrf_token']
        credential = request.form['credential']
        decoded_token = id_token.verify_oauth2_token(credential, requests.Request(), '1031925357556-g9tr3am18n1vg8ce88svenjgj82onrvt.apps.googleusercontent.com')

        # ID for student account to be used in all other calls
        userid = decoded_token['sub'] 
        userId = userid
        session['user_id'] = userid
        session['g_csrf_token'] = token
        
        # Email for student account to be used in all other calls
        email = decoded_token['email']
        
        # Student account name
        FName = decoded_token['given_name']
        LName = decoded_token['family_name']
        
        # Get profile ID, insert new profile if userId doesn't exist
        print("Retrieving user profile")
        profile = db.get_profile_by_id(str(userId))
        if profile == None:
            db.insert_new_profile(str(userId), FName, LName, email)

        home_page = make_response(redirect(url_for('home_page')))
        home_page.set_cookie('g_csrf_token', token)

        return home_page
    except ValueError:
        return redirect(url_for('login_page'))
    
@app.route('/map')
def map_page():
    global userId, favorites, addresses
    if isValidSession(userId):
        decks = get_parking_availability()
    
        # Pull favorites and addresses from database here

        # EXAMPLE
        # addresses = db.get_all_deck_info()
        # favorites = db.get_all_favorites_by_user(userId)

        return render_template('interactive_map.html', favData=favorites, deckData=decks, backDisplay=True, aboutDisplay=False)
    return redirect(url_for('login_page'))
    
@app.route('/classes')
def classes_page():
    global userId, classes
    if isValidSession(userId):
        classes = []
        classes = db.get_all_classes_by_user((userId,))
        print(classes)
        return render_template('classes.html', classData=classes, backDisplay=True, aboutDisplay=False)
    return redirect(url_for('login_page'))

@app.route('/add-classes', methods=['GET', 'POST'])
def add_classes_page():
    global userId, buildings
    if isValidSession(userId):
        if request.method == 'GET':
            return render_template('add_classes.html', buildingData=buildings, backDisplay=True, aboutDisplay=False)
        else:
            data = request.data.decode('utf-8')
            data = parse_qs(data)
            location = data['location']
            db.insert_new_class(str(userId), location[0])
            return render_template('add_classes.html', buildingData=buildings, backDisplay=True, aboutDisplay=False)
    return redirect(url_for('login_page'))

@app.route('/favorites')
def favorites_page():
    print("favorites_page")
    global userId, favorites
    if isValidSession(userId):
        # Pull all the favorites here

        # EXAMPLE
        favorites = db.get_all_favorites_by_user(userId)

        return render_template('favorites.html', favData=favorites, backDisplay=True, aboutDisplay=False)
    return redirect(url_for('login_page'))  

@app.route('/add-favorites', methods=['GET','POST'])
def add_favorites_page():
    print("add_favorites_page")
    global userId
    if isValidSession(userId):
        if request.method == 'GET':
            return render_template('add_favorites.html', backDisplay=True, aboutDisplay=False)
        else:
            # Put the code for adding a favorite here
            # use Javascript to POST to add_favorites.html
            # when Back button is pushed, redirect to favorites_page

            # EXAMPLE
            deck = request.form['deck'] 
             
            # populate fav object then pass to db function
            db.insert_new_favorite(fav)

            return redirect(url_for('favorites_page'))
    return redirect(url_for('login_page'))
    
@app.route('/alerts')
def alerts_page():
    print("alerts_page")
    global userId, alerts
    if isValidSession(userId):
        now = datetime.datetime.now()
        # alerts = db.get_alerts_by_date(now)

        return render_template('alerts.html', alertData=alerts, backDisplay=True, aboutDisplay=False)
    return redirect(url_for('login_page')) 
    
@app.route('/feedback', methods=['GET','POST'])
def feedback_page():
    print("feedback_page")
    global userId
    if isValidSession(userId):
        if request.method == 'GET':
            return render_template('feedback.html', backDisplay=True, aboutDisplay=False)
        else:
            # Put the code for sending a feedback to email here

            # user = request.form['userId']
            # feedback = request.form['feedback']
            # send_feedback(user, feedback)

            return render_template('feedback.html', backDisplay=True, aboutDisplay=False)
    return redirect(url_for('login_page'))    

def isValidSession(user_id):
    if (user_id != None) and ('user_id' in session) and (session['user_id'] == userId):
        print("User validated")
        return True
    return False




if __name__ == '__main__':
    print('starting app...')
    app.run(ssl_context='adhoc', debug=True, host=HOST, port=PORT)
    
