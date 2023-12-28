from flask import Flask, request, jsonify
import joblib
from sklearn.preprocessing import StandardScaler
import pickle
import numpy as np
from flask import render_template
import pandas as pd

app = Flask(__name__)
scaler=StandardScaler()
# Load the pre-trained machine learning model
model=pickle.load(open('D:\Hackathon Rajasthan\ANNmodel.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html')
# Endpoint for predicting fraud
@app.route('/predict', methods=['POST'])
def predict():
    # data = request.get_json()
    if request.method == 'POST':
        Unn=request.form['Unnamed']
        cc_num = request.form['cc_num']
        amt = request.form['amt']
        zip = request.form['zip']
        city_pop = request.form['city_pop']
        trans_num = request.form['trans_num']
        unix_time = request.form['unix_time']

     
    data = {'Unnamed':Unn,'cc_num': [cc_num], 'amt': [amt], 'zip': [zip], 'city_pop': [city_pop], 'trans_num': [trans_num], 'unix_time': [unix_time]}
    input_data = pd.DataFrame(data)

# Convert the DataFrame to a numpy array
    input_data_array = input_data.values

# Scale the input data using the same scaler used for training
    input_data_scaled = scaler.fit_transform(input_data_array)

# Make predictions using the model
    prediction = model.predict(input_data_scaled)
    if(prediction[0][0] > 0.5):
     result="Fraud"
    else:
     result="Not Fraud"
     
     if(result=="Fraud"):
      return render_template('fraud.html', result=result)
     else:
      return render_template('result.html', result=result)
    
   
if __name__ == '__main__':
    app.run(debug=True)
