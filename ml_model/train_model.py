import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle

def train_vehicle_prediction_model(data_file):
    # Load the dataset
    df = pd.read_csv(data_file)

    # Combine Time and Date into a DateTime column
    # Assuming Date is in format 'DD' and Time is in format 'HH:MM:SS AM/PM'
    # We'll assume the year is 2023 for simplicity (you can adjust this if needed)
    df['DateTime'] = pd.to_datetime(
        df['Date'].astype(str) + ' 2023 ' + df['Time'],
        format='%d %Y %I:%M:%S %p'
    )

    # Map 'Day of the week' to numerical values (0=Monday, 1=Tuesday, ..., 6=Sunday)
    day_mapping = {
        'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
        'Friday': 4, 'Saturday': 5, 'Sunday': 6
    }
    df['day_of_week'] = df['Day of the week'].map(day_mapping)

    # Extract features from DateTime
    df['hour'] = df['DateTime'].dt.hour
    df['month'] = df['DateTime'].dt.month

    # Features and target
    X = df[['hour', 'day_of_week', 'month']]
    y = df['Total']  # Use 'Total' as the target (previously 'Vehicles')

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save the model
    with open('ml_model/saved_model.pkl', 'wb') as f:
        pickle.dump(model, f)

    # Return the model's score on the test set
    return model.score(X_test, y_test)

def predict_vehicle_count(datetime_str):
    try:
        # Load the trained model
        with open('ml_model/saved_model.pkl', 'rb') as f:
            model = pickle.load(f)

        # Parse the input datetime
        dt = pd.to_datetime(datetime_str)

        # Extract features
        features = pd.DataFrame({
            'hour': [dt.hour],
            'day_of_week': [dt.dayofweek],
            'month': [dt.month]
        })

        # Make prediction
        prediction = model.predict(features)
        return prediction[0]
    except Exception as e:
        print(f"Error in prediction: {e}")
        return None