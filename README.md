python -m streamlit run app/soil_fertility_main.py


import streamlit as st
import pickle
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def get_clean_data(filepath="C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/Data/crop_recommendation.csv"):
    return pd.read_csv(filepath)

def add_sidebar():
    st.sidebar.header("Crop Recommendation Inputs")
    data = get_clean_data()
    
    slider_labels = [
        ("Nitrogen (N)", "N"), ("Phosphorus (P)", "P"), ("Potassium (K)", "K"),
        ("Temperature (°C)", "temperature"), ("Humidity (%)", "humidity"),
        ("pH Level", "ph"), ("Rainfall (mm)", "rainfall")
    ]

    # Create a dictionary of input values from sliders
    input_dict = {key: st.sidebar.slider(label, float(data[key].min()), float(data[key].max()), float(data[key].mean())) for label, key in slider_labels}
    return input_dict

def get_scaled_values(input_dict):
    data = get_clean_data()
    X = data[list(input_dict.keys())]
    
    scaled_dict = {key: (value - X[key].min()) / (X[key].max() - X[key].min()) for key, value in input_dict.items()}
    return scaled_dict

def get_radar_chart(input_data):
    """Generate a radar chart with multiple traces for different crop metrics."""
    input_data = get_scaled_values(input_data)
    categories = list(input_data.keys())

    fig = go.Figure()

    # Add trace for "Current Soil and Weather Conditions"
    fig.add_trace(go.Scatterpolar(
        r=list(input_data.values()),
        theta=categories,
        fill='toself',
        name='Current Conditions'
    ))

    # Hypothetical "Optimal Conditions" for comparison (example values)
    optimal_values = [0.6, 0.5, 0.7, 0.5, 0.6, 0.7, 0.8]
    fig.add_trace(go.Scatterpolar(
        r=optimal_values,
        theta=categories,
        fill='toself',
        name='Optimal Conditions'
    ))

    # Update layout for radar chart
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title="Crop Recommendation Radar Chart"
    )
    
    return fig

def add_predictions(input_data):
    """Load model, scaler, and label encoder, predict and display crop recommendation."""
    try:
        # Load the model, scaler, and label encoder
        model = pickle.load(open("C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/models/crop_recommendation_model.pkl", "rb"))
        scaler = pickle.load(open("C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/models/crop_recommendation_scaler.pkl", "rb"))
        label_encoder = pickle.load(open("C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/models/crop_recommendation_label_encoder.pkl", "rb"))
        
        # Convert input data to DataFrame for scaler compatibility
        input_df = pd.DataFrame([input_data], columns=input_data.keys())
        input_array_scaled = scaler.transform(input_df)
        
        # Predict recommended crop
        prediction = model.predict(input_array_scaled)
        predicted_crop = label_encoder.inverse_transform(prediction)[0]
        
        st.subheader("Recommended Crop")
        st.write(f"Based on the input conditions, the recommended crop is **{predicted_crop}**.")
        
    except (ValueError, IndexError, KeyError, TypeError) as e:
        st.error(f"An error occurred during prediction: {e}")
        st.write("Please ensure the model, scaler, and label encoder are correctly loaded and compatible with the input format.")

def main():
    st.set_page_config(
        page_title="Bhoomi: Crop Recommendation",
        layout="wide",
        page_icon="🌾",
        initial_sidebar_state="expanded"
    )
    input_data = add_sidebar()

    with st.container():
        st.title("Bhoomi: Crop Recommendation System")
        st.write("Adjust the sliders to reflect the soil and weather conditions of your field, and get a recommended crop.")

    col1, col2 = st.columns([3, 1])
    with col1:
        radar_chart = get_radar_chart(input_data)
        st.plotly_chart(radar_chart, use_container_width=True)
    with col2:
        add_predictions(input_data)

if __name__ == "__main__":
    main()

