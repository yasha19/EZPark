import datetime

# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

from google.oauth2 import id_token
from google.auth.transport import requests
from flask import Flask, render_template, request, make_response, redirect, url_for, session
from python.database.db import Database
from python.web.parking import get_parking_availability
from urllib.parse import parse_qs



app = Flask(__name__)
app.secret_key = 'uCraR5MZB/AvVo3Q24cBM/fZo5Kv/hV2HW9y0b3puClB25h0lbjBP6vYsHzz1hVY'
HOST, PORT = 'localhost', 8080
global userId, profile, buildings, favorites, classes, alerts, feedback, db, parking_decks, bus_locations
userId = None
profile = None
favorites = None
classes = None
alerts = None
feedback = None
db = Database()
buildings = db.get_all_buildings()
parking_decks = db.get_all_parking_decks()
bus_locations = db.get_all_bus_locations()


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


        # Get profile ID, insert new profile if userId doesn't exist
        profile = db.get_profile_by_id(userId)
        if profile == None or len(profile) == 0:
            # Email for student account to be used in all other calls
            email = decoded_token['email']
           
            # Student account name
            FName = decoded_token['given_name']
            LName = decoded_token['family_name']
           
            db.insert_new_profile(userId, FName, LName, email)


        home_page = make_response(redirect(url_for('home_page')))
        home_page.set_cookie('g_csrf_token', token)


        return home_page
    except ValueError:
        return redirect(url_for('login_page'))
   
@app.route('/map')
def map_page():
    global userId, parking_decks, classes, bus_locations
    if isValidSession(userId):
        courses = []
        lots = []
        classes = db.get_all_classes_by_user(userId)
        for class_ in classes:
            for building in buildings:
                if class_[1] == building[1]:
                    address = f'{building[2]}, {building[3]}, {building[4]} {building[5]}'
                    newClass = class_ + (address,)
                    courses.append(newClass)


        for lot in parking_decks:
            lotAddress = f'{lot[2]}, {lot[3]}, {lot[4]} {lot[5]}'
            newLot = (lot[1],) + (lotAddress,) + (lot[7],)
            lots.append(newLot)
        print(lots)


        return render_template('interactive_map.html', classData=courses, parkingData=lots, busData=bus_locations, backDisplay=True, aboutDisplay=False)
    return redirect(url_for('login_page'))
   
@app.route('/classes', methods=['GET'])
def classes_home_page():
    global userId, classes
    if isValidSession(userId):
        classes = db.get_all_classes_by_user(userId)
        return render_template('classes.html', classData=classes, buildingData=buildings, backDisplay=True, aboutDisplay=False)
    return redirect(url_for('login_page'))
   
@app.route('/classes', methods=['DELETE'])
def delete_classes():
    global userId, classes
    if isValidSession(userId):
        data = request.data.decode('utf-8')
        data = parse_qs(data)
        course = data['course']
        location = data['location']
        db.delete_class(userId, course[0], location[0])
        classes = db.get_all_classes_by_user(userId)
        return render_template('classes.html', classData=classes, buildingData=buildings, backDisplay=True, aboutDisplay=False)
    return redirect(url_for('login_page'))


@app.route('/add-classes', methods=['GET'])
def add_classes_home_page():
    global userId, buildings
    if isValidSession(userId):
        return render_template('add_classes.html', buildingData=buildings, backDisplay=True, aboutDisplay=False)
    return redirect(url_for('login_page'))


@app.route('/add-classes', methods=['POST'])
def add_classes():
    global userId, buildings
    if isValidSession(userId):
        data = request.data.decode('utf-8')
        data = parse_qs(data)
        course = data['course']    
        location = data['location']
        db.insert_new_class(userId, course[0], location[0])
        return render_template('add_classes.html', buildingData=buildings, backDisplay=True, aboutDisplay=False)
    return redirect(url_for('login_page'))


@app.route('/favorites', methods=['GET'])
def favorites_home_page():
    global userId, favorites
    if isValidSession(userId):
        favorites = db.get_all_favorites_by_user(userId)
        return render_template('favorites.html', favData=favorites, parkingData=parking_decks, backDisplay=True, aboutDisplay=False)
    return redirect(url_for('login_page'))


@app.route('/favorites', methods=['DELETE'])
def delete_favorites():
    global userId, favorites
    if isValidSession(userId):
        data = request.data.decode('utf-8')
        data = parse_qs(data)
        location = data['location']
        capacity = data['capacity']
        db.delete_favorite(userId, location[0], capacity[0])
        favorites = db.get_all_favorites_by_user(userId)
        return render_template('favorites.html', favData=favorites, parkingData=parking_decks, backDisplay=True, aboutDisplay=False)
    return redirect(url_for('login_page'))


@app.route('/add-favorites', methods=['GET'])
def add_favorites_home_page():
    global userId, parking_decks
    if isValidSession(userId):
        return render_template('add_favorites.html', parkingData=parking_decks, backDisplay=True, aboutDisplay=False)
    return redirect(url_for('login_page'))


@app.route('/add-favorites', methods=['POST'])
def add_favorites():
    global userId, parking_decks
    if isValidSession(userId):
        data = request.data.decode('utf-8')
        data = parse_qs(data)
        location = data['location']
        capacity = data['capacity']
        db.insert_new_favorite(userId, location[0], capacity[0])
        return render_template('add_favorites.html', parkingData=parking_decks, backDisplay=True, aboutDisplay=False)
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
    global userId, feedback, profile
    if isValidSession(userId):
        if request.method == 'GET':
            return render_template('feedback.html', profileData=profile, backDisplay=True, aboutDisplay=False)
        else:
            data = request.data.decode('utf-8')
            data = parse_qs(data)
            feedback = data['feedback']
            profile = db.get_profile_by_id(userId, feedback[0])
            return render_template('feedback.html', profileData=profile, backDisplay=True, aboutDisplay=False)
    return redirect(url_for('feedback_page'))

# def send_feedback_email(feedback_text):
#     receiver_email = 'recipient@example.com'  # Update with the recipient's email

#     message = MIMEMultipart()
#     message['From'] = SENDER_EMAIL
#     message['To'] = receiver_email
#     message['Subject'] = 'Feedback Submission'



def isValidSession(user_id):
    if (user_id != None) and ('user_id' in session) and (session['user_id'] == userId):
        print("User validated")
        return True
    return False






if __name__ == '__main__':
    print('starting app...')
    app.run(ssl_context='adhoc', debug=True, host=HOST, port=PORT)



            
