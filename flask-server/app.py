import time, json
from flask import Flask, request, jsonify
import pickle
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import joblib
import json
import sklearn
import numpy as np
from sklearn.metrics import accuracy_score
import boto3
from botocore.exceptions import NoCredentialsError
import requests
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def download_model_from_s3(bucket_name, file_key, local_path):
    aws_access_key_id='#'
    aws_secret_access_key='#'
    aws_session_token=None

    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      aws_session_token=aws_session_token)

    try:
        # Download the file from S3
        s3.download_file('ids-data-raw', 'rf_model.joblib', 'rf_model_s3_bucket.joblib')
        print(f"Model downloaded successfully to {local_path}")
    except NoCredentialsError:
        print("Credentials not available")
    except Exception as e:
        print(f"Error downloading model: {e}")

def read_csv_from_s3(bucket_name, file_key):
    # Set up AWS credentials and session
    aws_access_key_id='#'
    aws_secret_access_key='#'
    aws_session_token=None

    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      aws_session_token=aws_session_token)

    try:
        # Read the CSV file directly from S3 into a Pandas DataFrame
        obj = s3.get_object(Bucket=bucket_name, Key=file_key)
        df = pd.read_csv(obj['Body'])
        print(f"Data loaded successfully from {bucket_name}/{file_key}")
        return df
    except NoCredentialsError:
        print("Credentials not available")
    except Exception as e:
        print(f"Error reading data: {e}")

@app.route("/createPlots")
def create():
    download_model_from_s3('ids-data-raw', 'rf_model.joblib', 'rf_model_s3_bucket.joblib')
    data = read_csv_from_s3('ids-data-raw', 'X_test.csv')
    labels = read_csv_from_s3('ids-data-raw', 'y_test.csv')
    # Load the model using joblib
    loaded_model = joblib.load('rf_model_s3_bucket.joblib')
    predictions = loaded_model.predict(data.to_numpy())
    acc = np.round(accuracy_score(labels, predictions),3) * 100
    print(acc)
    probabilities = loaded_model.predict_proba(data.to_numpy())
    attacks = {0: 'BENIGN', 1: 'Botnet', 2: 'Botnet - Attempted', 3: 'DDoS', 4: 'DoS GoldenEye', 5: 'DoS GoldenEye - Attempted', 6: 'DoS Hulk', 7: 'DoS Hulk - Attempted', 8: 'DoS Slowhttptest', 9: 'DoS Slowhttptest - Attempted', 10: 'DoS Slowloris', 11: 'DoS Slowloris - Attempted', 12: 'FTP-Patator', 13: 'FTP-Patator - Attempted', 14: 'Heartbleed', 15: 'Infiltration', 16: 'Infiltration - Attempted', 17: 'Infiltration - Portscan', 18: 'Portscan', 19: 'SSH-Patator', 20: 'SSH-Patator - Attempted', 21: 'Web Attack - Brute Force', 22: 'Web Attack - Brute Force - Attempted', 23: 'Web Attack - SQL Injection', 24: 'Web Attack - SQL Injection - Attempted', 25: 'Web Attack - XSS', 26: 'Web Attack - XSS - Attempted'}
    return 

@app.route("/members")
def members():
    return {"members": ["hiren", "zero"]}

@app.route('/time')
def get_current_time():
    return {'time': time.time()}
    
@app.route('/plot-bar')
def plot_bar():
    labels = pd.read_csv('labels.csv')
    fig = px.bar(labels.iloc[:7], x="Label", y="Count", barmode="group")
    graphJSON = plotly.io.to_json(fig, pretty=True)
    return graphJSON

@app.route('/bar-binary')
def plot_binary_bar():
    labels = pd.read_csv('binary_data.csv')
    fig = px.bar(labels, x="Label", y="Count")
    graphJSON = plotly.io.to_json(fig, pretty=True)
    return graphJSON

@app.route('/pie-chart-data')
def get_pie_chart_data():
    # Replace this with your data or data retrieval logic
    labels = pd.read_csv('labels.csv')
    fig = px.pie(labels, names='Label', values='Count', title='Pie Chart showing intrusion types', hole = 0.4)
    fig.update_traces(marker = dict(line = dict(color = 'black', width = 0.5)), rotation=0, textposition='inside', textinfo='percent+label')
    graphJSON = plotly.io.to_json(fig, pretty=True)
    return graphJSON

@app.route('/pie-binary')
def get_binary_pie_chart_data():
    # Replace this with your data or data retrieval logic
    labels = pd.read_csv('binary_data.csv')
    fig = px.pie(labels, names='Label', values='Count', title='Pie Chart showing intrusion types', hole = 0.4)
    fig.update_traces(marker = dict(line = dict(color = 'black', width = 0.5)), rotation=0, textposition='inside', textinfo='percent+label')
    graphJSON = plotly.io.to_json(fig, pretty=True)
    return graphJSON

@app.route('/predict')
def predict():        
    # Get data from the frontend
    download_model_from_s3('ids-data-raw', 'rf_model.joblib', 'rf_model_s3_bucket.joblib')
    data = read_csv_from_s3('ids-data-raw', 'X_test.csv')
    labels = read_csv_from_s3('ids-data-raw', 'y_test.csv')
    # Load the model using joblib
    loaded_model = joblib.load('rf_model_s3_bucket.joblib')
    predictions = loaded_model.predict(data.to_numpy())
    acc = np.round(accuracy_score(labels, predictions),3) * 100
    print(acc)
    probabilities = loaded_model.predict_proba(data.to_numpy())
    attacks = {0: 'BENIGN', 1: 'Botnet', 2: 'Botnet - Attempted', 3: 'DDoS', 4: 'DoS GoldenEye', 5: 'DoS GoldenEye - Attempted', 6: 'DoS Hulk', 7: 'DoS Hulk - Attempted', 8: 'DoS Slowhttptest', 9: 'DoS Slowhttptest - Attempted', 10: 'DoS Slowloris', 11: 'DoS Slowloris - Attempted', 12: 'FTP-Patator', 13: 'FTP-Patator - Attempted', 14: 'Heartbleed', 15: 'Infiltration', 16: 'Infiltration - Attempted', 17: 'Infiltration - Portscan', 18: 'Portscan', 19: 'SSH-Patator', 20: 'SSH-Patator - Attempted', 21: 'Web Attack - Brute Force', 22: 'Web Attack - Brute Force - Attempted', 23: 'Web Attack - SQL Injection', 24: 'Web Attack - SQL Injection - Attempted', 25: 'Web Attack - XSS', 26: 'Web Attack - XSS - Attempted'}
    data['Potential Threat'] = predictions
    prob = [np.round(max(probabilities[i]), 4) for i in range(len(probabilities))]
    data['Probability of the Potential Threat'] = prob
    data['Actual'] = labels
    df = pd.DataFrame(predictions)
    # attack_names = df.map(attacks)
    # , 'Predicted Attack Name': attack_names
    result_df = pd.DataFrame({'Prediction': predictions[:20].reshape(-1),'Probability of Potential Threat': np.array(prob)[:20].reshape(-1), 'Actual': labels[:20].to_numpy().reshape(-1)})
    result_json = {
        'prediction': result_df['Prediction'].tolist(),
        # 'attack_name': result_df['Predicted Attack Name'].tolist(),
        'probability': result_df['Probability of Potential Threat'].tolist(),
        'actual': result_df['Actual'].tolist(),
        'accuracy': acc
    }

    # Return predictions as JSON
    return jsonify(result_json)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5000, debug=True)
