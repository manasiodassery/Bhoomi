import streamlit as st
import pickle
import pandas as pd
import numpy as np

def get_clean_data(filepath="C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/Data/price_forecasting.csv"):
    return pd.read_csv(filepath)

def add_sidebar():
    st.sidebar.header("Price Forecasting Inputs")
    data = get_clean_data()
    
    # Dropdown options for each selection
    state = st.sidebar.selectbox("Select State", data['State'].unique())
    district = st.sidebar.selectbox("Select District", data[data['State'] == state]['District'].unique())
    market = st.sidebar.selectbox("Select Market", data[(data['State'] == state) & (data['District'] == district)]['Market'].unique())
    commodity = st.sidebar.selectbox("Select Commodity", data[(data['State'] == state) & (data['District'] == district) & (data['Market'] == market)]['Commodity'].unique())
    
    input_data = {
        "State": state,
        "District": district,
        "Market": market,
        "Commodity": commodity
    }
    return input_data

def encode_categorical(data):
    # Label encode non-numeric columns
    for column in data.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        data[column] = le.fit_transform(data[column])
    return data

def preprocess_input(input_data, data):
    # Convert input data to a DataFrame with the same columns as the dataset
    input_df = pd.DataFrame([input_data])
    
    # Concatenate input_df with data for consistent encoding
    combined_data = pd.concat([data, input_df], ignore_index=True)
    combined_data = encode_categorical(combined_data)
    
    # Extract only the last row, which is our user input after encoding
    input_encoded = combined_data.iloc[[-1]]
    return input_encoded.drop(['Modal_x0020_Price', 'Price_Trend'], axis=1)

def add_predictions(input_data):
    """Load models, preprocess input, predict and display results."""
    try:
        # Load models and scaler
        price_model = pickle.load(open("C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/models/price_forecasting_model.pkl", "rb"))
        trend_model = pickle.load(open("C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/models/price_trend_model.pkl", "rb"))
        scaler = pickle.load(open("C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/models/price_forecasting_scaler.pkl", "rb"))
        
        # Load the data for preprocessing and encoding
        data = get_clean_data()
        input_encoded = preprocess_input(input_data, data)
        
        # Scale the input data
        input_scaled = scaler.transform(input_encoded)
        
        # Make predictions
        price_prediction = price_model.predict(input_scaled)
        trend_prediction = trend_model.predict(input_scaled)
        
        # Display results
        st.subheader("Price Forecasting Results")
        st.write(f"Forecasted Price: ₹{price_prediction[0]:.2f}")
        st.write(f"Price Trend: {'Up' if trend_prediction[0] == 'Up' else 'Down'}")
        
    except (ValueError, IndexError, KeyError, TypeError) as e:
        st.error(f"An error occurred during prediction: {e}")
        st.write("Please ensure the model, scaler, and data are correctly loaded and compatible with the input format.")

def main():
    st.set_page_config(
        page_title="Bhoomi: Price Forecasting System",
        layout="wide",
        page_icon="📈",
        initial_sidebar_state="expanded"
    )
    input_data = add_sidebar()

    with st.container():
        st.title("Bhoomi: Price Forecasting System")
        st.write("Select the location and commodity to view the forecasted price.")

    add_predictions(input_data)

if __name__ == "__main__":
    main()

