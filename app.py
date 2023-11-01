#!/usr/bin/env python3

from flask import Flask, render_template
from python.utils.session import Sessions
from python.database.db import Database

app = Flask(__name__)
HOST, PORT = 'localhost', 8080
global username, favorites, classes, alerts
global backDisplay
backDisplay= True
db = Database()
sessions = Sessions()

@app.route('/')
def index_page():
    return render_template('login.html', backDisplay=False, aboutDisplay=False, settingsDisplay=True, logDisplay=True)

@app.route('/login')
def login_page():
    return render_template('login.html', backDisplay=False, aboutDisplay=False, settingsDisplay=True, logDisplay=True)

@app.route('/logout')
def logout_page():
    return render_template('login.html', backDisplay=False, aboutDisplay=False, settingsDisplay=True, logDisplay=True)
    
@app.route('/about')
def about_page():
    return render_template('about.html', backDisplay=False, aboutDisplay=False)

@app.route('/home')
def home_page():
    return render_template('home.html', backDisplay=False, aboutDisplay=True)

@app.route('/map')
def map_page():
    return render_template('interactive_map.html', backDisplay=True, aboutDisplay=False)

@app.route('/add-classes')
def classes_page():
    return render_template('add_classes.html', backDisplay=True, aboutDisplay=False)

@app.route('/add-classes', methods=['POST'])
def add_classes_page():
    return render_template('add_classes.html', backDisplay=True, aboutDisplay=False)

@app.route('/add-favorites')
def favorites_page():
    return render_template('add_favorites.html', backDisplay=True, aboutDisplay=False)

@app.route('/add-favorites', methods=['POST'])
def add_favorites_page():
    return render_template('add_favorites.html', backDisplay=True, aboutDisplay=False)

@app.route('/alerts')
def alerts_page():
    return render_template('alerts.html', backDisplay=True, aboutDisplay=False)

@app.route('/feedback')
def feedback_page():
    return render_template('feedback.html', backDisplay=True, aboutDisplay=False)

if __name__ == '__main__':
    app.run(ssl_context='adhoc', debug=True, host=HOST, port=PORT)
