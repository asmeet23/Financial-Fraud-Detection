from flask import Flask, request, jsonify, render_template, url_for, g
import sqlite3
import threading
import time
import json
import random
import pandas as pd
import geocoder
from sklearn.preprocessing import StandardScaler, LabelEncoder
from keras.models import load_model
from flask_socketio import SocketIO, emit
import pickle
from threading import Thread

app = Flask(__name__)

encoder = LabelEncoder()
scaler = pickle.load(open('min_max_scaler.pkl', 'rb'))
model = load_model('my_model.h5')
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/graph')
def graph1():
    return render_template('DynamicGraph.html', css=url_for('static', filename='Dynamicgraph.css'))

def generate_transaction():
    df = pd.read_csv('fraudTrain_clean.csv')
    for i, row in df.iterrows():
        try:
            transaction = {
                'cc_num': row['cc_num'],
                'amt': row['amt'],
                'zip': row['zip'],
                'lat': row['lat'],
                'long': row['long'],
                'trans_num': row['trans_num'],
                'is_fraud': row['is_fraud'],
                'trans_date': row['trans_date'],
                'trans_time': row['trans_time']
            }
            socketio.emit('transaction', json.dumps(transaction))
            time.sleep(random.uniform(0, 2))
        except Exception as e:
            print(f"Error generating transaction: {e}")

@app.route('/Live')
def transaction():
    thread = Thread(target=generate_transaction)
    thread.start()
    return render_template('Live.html')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('Newdata.db')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

with app.app_context():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS userdata (
            name TEXT,
            Bank_acc_no INTEGER,
            Unn INTEGER,
            cc_num INTEGER,
            amount INTEGER,
            zip INTEGER,
            city_pop INTEGER,
            trans_num INTEGER,
            Lattitude REAL,
            Longitude REAL,
            unix_time INTEGER,
            prediction INTEGER,
            result TEXT
        )
    ''')
    db.commit()

@app.route('/')
def home():
    return render_template('login.html', css=url_for('static', filename='login.css'))

@app.route('/route_to_dashboard')
def route_to_dashboard():
    return render_template('dashboard.html', css=url_for('static', filename='dash.css'))

@app.route('/about')
def about():
    return render_template('About.html', css=url_for('static', filename='About.css'))

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name', False)
    Unn = request.form.get('Unnamed', False)
    cc_num = request.form.get('cc_num', False)
    amt = request.form.get('amt', False)
    zip = request.form.get('zip', False)
    city_pop = request.form.get('city_pop', False)
    trans_num = request.form.get('trans_num', False)
    unix_time = request.form.get('unix_time', False)
    ans = encoder.fit_transform([trans_num])
    
    g = geocoder.ip('me')
    if g.latlng:
        latitude, longitude = g.latlng

    Bank_acc_no = random.randint(1000000000, 9999999999)
    
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        data = {'Unnamed': Unn, 'cc_num': [cc_num], 'amt': [amt], 'zip': [zip], 'city_pop': [city_pop], 'trans_num': [ans], 'unix_time': [unix_time]}
        input_data = pd.DataFrame(data)
        input_data = np.array(input_data).reshape(1, -1)
        input_data_scaled = scaler.transform(input_data)
        prediction = model.predict(input_data_scaled)
        RP = round(prediction[0][0])
        result = "Fraud" if prediction[0][0] > 0.3 else "Not Fraud"

        if name and Unn:
            cursor.execute('INSERT INTO userdata (name, Bank_acc_no, Unn, cc_num, amount, zip, city_pop, trans_num, Lattitude, Longitude, unix_time, prediction, result) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (name, Bank_acc_no, Unn, cc_num, amt, zip, city_pop, trans_num, latitude, longitude, unix_time, RP, result))
            db.commit()

        return render_template('index.html', prediction=prediction[0][0], result=result, css=url_for('static', filename='index.css'))

@app.route('/data')
def display_data():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT name, Bank_acc_no, cc_num, amount, trans_num, result FROM userdata')
        data = cursor.fetchall()
    return render_template('display.html', data=data)

@app.route('/delete', methods=['POST'])
def delete_data():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM userdata')
        db.commit()
    return render_template('display.html')

@app.route('/manage')
def onlyFraud():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT name, Bank_acc_no, cc_num, amount, trans_num, result FROM userdata WHERE result = "Fraud"')
        fraud_transactions = cursor.fetchall()
    return render_template('manage.html', transactions=fraud_transactions)

@app.route('/map')
def index():
    g = geocoder.ip('me')
    lat, lng = g.latlng
    m = folium.Map(location=[lat, lng])
    folium.Marker([lat, lng], popup='Your Location').add_to(m)
    m.save('static/map.html')
    return render_template('map.html')

@app.route('/details_template/<name>')
def details_template(name):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM userdata WHERE name = ?', (name,))
        details = cursor.fetchone()
    return render_template('details.html', details=details)


