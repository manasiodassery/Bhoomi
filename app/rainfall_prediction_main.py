import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
import joblib

# Load your trained model and preprocessors
model = load_model('path_to_your_saved_model.h5')
scaler = joblib.load('path_to_your_saved_scaler.pkl')
label_encoder = joblib.load('path_to_your_saved_encoder.pkl')

def get_user_input():
    st.sidebar.header("Input Parameters for Rainfall Prediction")
    # Create sliders and input fields
    temperature = st.sidebar.slider('Average Temperature (°C)', 10.0, 40.0, 25.0)
    humidity = st.sidebar.slider('Average Humidity (%)', 0.0, 100.0, 50.0)
    wind_speed = st.sidebar.slider('Wind Speed (m/s)', 0.0, 15.0, 5.0)
    pressure = st.sidebar.slider('Atmospheric Pressure (hPa)', 950.0, 1050.0, 1000.0)
    season = st.sidebar.selectbox('Season', ['Winter', 'Spring', 'Summer', 'Autumn'])
    
    # Prepare user input array
    return np.array([[temperature, humidity, wind_speed, pressure, season]])

def preprocess_input(input_data):
    # Assuming all inputs except 'season' are numerical and need scaling
    numerical_input = scaler.transform(input_data[:, :-1])
    # Assuming 'season' is categorical and needs encoding
    categorical_input = label_encoder.transform(input_data[:, -1]).reshape(-1, 1)
    return np.hstack((numerical_input, categorical_input))

def show_prediction(prediction):
    st.subheader('Predicted Probability of Rainfall')
    st.write(f"Probability of Rainfall: {prediction[0]*100:.2f}%")

def main():
    st.title("Rainfall Probability Prediction App")
    input_data = get_user_input()
    preprocessed_input = preprocess_input(input_data)
    prediction = model.predict(preprocessed_input)
    show_prediction(prediction)

if __name__ == '__main__':
    main()
