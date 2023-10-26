from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host='sql9.freesqldatabase.com',
    user='sql9656653',
    password='TiLR6twahS',
    database='sql9656653'
)

@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM profile')
    data = cursor.fetchall()
    print(data)
    cursor.close()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run()