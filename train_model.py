# ml_model/train_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle

def train_vehicle_prediction_model(data_file):
    df = pd.read_csv(data_file)
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    
    df['hour'] = df['DateTime'].dt.hour
    df['day_of_week'] = df['DateTime'].dt.dayofweek
    df['month'] = df['DateTime'].dt.month
    
    X = df[['hour', 'day_of_week', 'month']]
    y = df['Vehicles']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    with open('ml_model/saved_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    return model.score(X_test, y_test)

def predict_vehicle_count(datetime_str):
    with open('ml_model/saved_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    dt = pd.to_datetime(datetime_str)
    features = pd.DataFrame({
        'hour': [dt.hour],
        'day_of_week': [dt.dayofweek],
        'month': [dt.month]
    })
    
    prediction = model.predict(features)
    return prediction[0]