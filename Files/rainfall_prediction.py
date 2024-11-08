import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import joblib
import logging

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(filepath):
    try:
        data = pd.read_csv(filepath)
        data.columns = [col.strip() for col in data.columns]  # Strip any extra whitespace from headers
        if 'Date' not in data.columns:
            logging.error("Missing 'Date' column in dataset.")
            return pd.DataFrame()  # Return empty DataFrame if 'Date' column is missing
        data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')  # Adjust format if necessary
        logging.info("Data loaded successfully with shape: {}".format(data.shape))
        return data
    except Exception as e:
        logging.error("Failed to load data: {}".format(e))
        return pd.DataFrame()  # Return empty DataFrame on error

def prepare_data(data):
    try:
        scaler = MinMaxScaler()
        label_encoder = LabelEncoder()
        
        features = ['Temperature', 'Humidity', 'Wind_Speed', 'Pressure']
        data[features] = scaler.fit_transform(data[features])
        data['Season_encoded'] = label_encoder.fit_transform(data['Season'])
        
        X = data[['Temperature', 'Humidity', 'Wind_Speed', 'Pressure', 'Season_encoded']]
        y = data['Rainfall']
        return train_test_split(X, y, test_size=0.2), scaler, label_encoder
    except KeyError as e:
        logging.error("Missing columns in data preparation: {}".format(e))
        exit(1)  # Exit if data preparation fails

def build_model(input_dim):
    model = Sequential([
        Dense(100, activation='relu', input_dim=input_dim),
        Dropout(0.2),
        Dense(50, activation='relu'),
        Dropout(0.2),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

def train_model(model, X_train, y_train):
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    model.fit(X_train, y_train, epochs=100, validation_split=0.2, verbose=1, callbacks=[early_stopping])
    logging.info("Model training complete.")

def save_model(scaler, label_encoder, model):
    model_path = 'C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/models/rainfall_prediction_model.h5'
    scaler_path = 'C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/models/rainfall_scaler.pkl'
    encoder_path = 'C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/models/rainfall_label_encoder.pkl'
    
    joblib.dump(scaler, scaler_path)
    joblib.dump(label_encoder, encoder_path)
    model.save(model_path)
    logging.info("Model, scaler, and label encoder saved successfully.")

def make_prediction(model, scaler, label_encoder, inputs):
    try:
        num_inputs = scaler.transform([inputs[:4]])
        cat_input = label_encoder.transform([inputs[4]])
        all_inputs = np.hstack((num_inputs, cat_input.reshape(-1, 1)))
        prediction = model.predict(all_inputs)
        return prediction
    except Exception as e:
        logging.error("Error making prediction: {}".format(e))
        return None

def main():
    data = load_data("C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/Data/rainfall_prediction.csv")
    if not data.empty:
        (X_train, X_test, y_train, y_test), scaler, label_encoder = prepare_data(data)
        model = build_model(X_train.shape[1])
        train_model(model, X_train, y_train)
        save_model(scaler, label_encoder, model)

        # Simulate user input
        user_input = [25.0, 50.0, 5.0, 1000.0, 'Winter']
        prediction = make_prediction(model, scaler, label_encoder, user_input)
        if prediction is not None:
            logging.info("Predicted Rainfall: {}".format(prediction[0]))

if __name__ == '__main__':
    main()
