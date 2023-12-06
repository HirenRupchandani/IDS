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

def download_model_from_s3(bucket_name, file_key, local_path):
    aws_access_key_id='AKIAU6EA3JVX5E7IDAG3'
    aws_secret_access_key='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'
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
    aws_access_key_id='AKIAU6EA3JVX5E7IDAG3'
    aws_secret_access_key='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'
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


app = Flask(__name__)

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
    app.run(debug=True)