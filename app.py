from flask import Flask, request, jsonify,request, g
import sqlite3
from sklearn.preprocessing import StandardScaler
import pickle
import numpy as np
from flask import render_template
import pandas as pd
import random
from flask import url_for
from sklearn.preprocessing import LabelEncoder
from keras.models import load_model
import folium
import geocoder

app = Flask(__name__)

encoder=LabelEncoder()

scaler=pickle.load(open('min_max_scaler.pkl','rb'))
# Load the pre-trained machine learning model
model=load_model('my_model.h5')


#code for the sql insertion view and deletion of the data
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('Newdata.db')
    return db

# Function to close the database connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Create table if it doesn't exist
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
            prediction Integer,
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
    return render_template('About.html',css=url_for('static', filename='About.css'))

# @app.route('/data')
# def data():
#        return render_template('display.html', css=url_for('static', filename='display.css'))

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name',False)
    Unn = request.form.get('Unnamed',False)
    cc_num = request.form.get('cc_num',False)
    amt = request.form.get('amt',False)
    zip = request.form.get('zip',False)
    city_pop = request.form.get('city_pop',False)
    trans_num = request.form.get('trans_num',False)
    unix_time = request.form.get('unix_time',False)
    ans=encoder.fit_transform([trans_num])
    # ans=trans_num
    
    g = geocoder.ip('me')
    if g.latlng:
     latitude, longitude = g.latlng
 
     Bank_acc_no=random.randint(1000000000,9999999999)
     Bank_acc_no=Bank_acc_no
   
    # Insert the form data into the database
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        data = {'Unnamed':Unn,'cc_num': [cc_num], 'amt': [amt], 'zip': [zip], 'city_pop': [city_pop], 'trans_num': [ans], 'unix_time': [unix_time]}
        input_data = pd.DataFrame(data)
        print(data)
        input_data = np.array(input_data).reshape(1, -1)
        input_data_scaled = scaler.transform(input_data)
        prediction= model.predict(input_data_scaled)
        RP=round(prediction[0][0])
        # print("ans:",ans)
        # print("prediction-->",prediction[0][0])
        if(prediction[0][0]>0.3):
         result="Fraud"
        else:
         result="Not Fraud"
        
             
        # Bank_acc_no=random.randint(1000000000,9999999999)
         
        cursor.execute('INSERT INTO userdata (name,Bank_acc_no, Unn, cc_num, amount, zip, city_pop, trans_num,Lattitude,Longitude,unix_time,prediction,result) VALUES (?, ?, ?, ?, ?,?, ?,?, ?,?,?,?,?)', (name,Bank_acc_no, Unn, cc_num, amt, zip, city_pop, trans_num,latitude,longitude,unix_time,RP,result))
        db.commit()
        return render_template('index.html', prediction=prediction[0][0],result=result, css=url_for('static', filename='index.css'))
 

# Route for displaying the data
@app.route('/data')
def display_data():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT name, Bank_acc_no,cc_num,amount,trans_num,result FROM userdata')
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

@app.route('/details_template/<name>')
def details_template(name):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM userdata WHERE name = ?', (name,))
        details = cursor.fetchone()

    return render_template('details.html', details=details)
   
if __name__ == '__main__':
    app.run(debug=True)
