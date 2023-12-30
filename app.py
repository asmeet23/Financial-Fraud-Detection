from flask import Flask, request, jsonify,request, g
import sqlite3
import joblib
from sklearn.preprocessing import StandardScaler
import pickle
import numpy as np
from flask import render_template
import pandas as pd
import random
from flask import url_for

app = Flask(__name__)

scaler=StandardScaler()
# Load the pre-trained machine learning model
model=pickle.load(open(r'C:\Users\basim\RJPOLICE_HACK_1474_A-team_7\ANNmodel.pkl','rb'))


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
            Unn TEXT,
            cc_num TEXT,
            amount INTEGER,
            zip INTEGER,
            city_pop INTEGER,
            trans_num INTEGER,
            unix_time INTEGER,
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

# @app.route('/submit')
# def home():
#        return render_template('index.html', css=url_for('static', filename='index.css'))

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name',False)
    Unn = request.form.get('Unnamed',False)
    cc_num = request.form.get('cc_num',False)
    amt = request.form.get('amt',False)
    zip = request.form.get('zip',False)
    city_pop = request.form.get('city_pop',False)
    trans_num = random.randint(1000000000, 9999999999)
    unix_time = request.form.get('unix_time',False)

    # Generate a random transaction number 
   

    # Insert the form data into the database
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        Unn2=Unn
        cc_num2=cc_num
        amt2=amt
        zip2=zip
        city_pop2=city_pop
        trans_num2=trans_num
        unix_time2=unix_time
        
        data = {'Unnamed':Unn2,'cc_num': [cc_num2], 'amt': [amt2], 'zip': [zip2], 'city_pop': [city_pop2], 'trans_num': [trans_num2], 'unix_time': [unix_time2]}
        input_data = pd.DataFrame(data)
        input_data_array = input_data.values
        
# Scale the input data using the same scaler used for training
        input_data_scaled = scaler.fit_transform(input_data_array)

# Make predictions using the model
        prediction = model.predict(input_data_scaled)
        if(prediction[0][0] > 0.5):
         result="Fraud"
        else:
         result="Not Fraud"
         
        cursor.execute('INSERT INTO userdata (name, Unn, cc_num, amount, zip, city_pop, trans_num,unix_time,result) VALUES (?, ?, ?, ?, ?, ?, ?,?,?)', (name, Unn, cc_num, amt, zip, city_pop, trans_num,unix_time,result))
        db.commit()
        
    # Retrieve data including 'result' column
        cursor.execute('SELECT name, cc_num, amount, zip, trans_num, unix_time, result FROM userdata')
        data = cursor.fetchall()

# Pass the data to the template
        return render_template('display.html', data=data)
 

# Route for displaying the data
@app.route('/data')
def display_data():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM userdata')
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














# # Endpoint for predicting fraud
# @app.route('/predict', methods=['POST'])
# def predict():
#     # data = request.get_json()
#     if request.method == 'POST':
#         Unn=request.form['Unnamed']
#         cc_num = request.form['cc_num']
#         amt = request.form['amt'] 
#         zip = request.form['zip']
#         city_pop = request.form['city_pop']
#         trans_num = request.form['trans_num']
#         unix_time = request.form['unix_time']

     
#     data = {'Unnamed':Unn,'cc_num': [cc_num], 'amt': [amt], 'zip': [zip], 'city_pop': [city_pop], 'trans_num': [trans_num], 'unix_time': [unix_time]}
#     input_data = pd.DataFrame(data)

# # Convert the DataFrame to a numpy array
#     input_data_array = input_data.values

# # Scale the input data using the same scaler used for training
#     input_data_scaled = scaler.fit_transform(input_data_array)

# # Make predictions using the model
#     prediction = model.predict(input_data_scaled)
#     if(prediction[0][0] > 0.5):
#      result="Fraud"
#     else:
#      result="Not Fraud"
     
#      return result
    
   
if __name__ == '__main__':
    app.run(debug=True)
