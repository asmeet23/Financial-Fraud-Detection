import requests

# Sample data to be sent for prediction
data = {
    'features': [0,2703186189652095,4.97,28654,3495,56438,1325376018]  # Replace with your feature values
}

# Send a POST request to the Flask app
response = requests.post('http://127.0.0.1:5000/predict', json=data)

if response.status_code == 200:
    print(response.json())
else:
    print("Error:", response.status_code)

