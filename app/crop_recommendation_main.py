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

def get_bar_chart(input_data):
    """Generate a bar chart displaying only current input conditions."""
    # Scale input data for display
    scaled_input = get_scaled_values(input_data)
    
    # Prepare data for bar chart
    categories = list(scaled_input.keys())
    input_values = list(scaled_input.values())

    # Create a bar chart using Plotly
    fig = go.Figure(data=[
        go.Bar(name='Current Conditions', x=categories, y=input_values)
    ])

    # Update layout for bar chart
    fig.update_layout(
        title="Current Input Conditions",
        xaxis_title="Metrics",
        yaxis_title="Scaled Values",
        yaxis=dict(range=[0, 1])
    )
    
    return fig

def get_scaled_values(input_dict):
    data = get_clean_data()
    X = data[list(input_dict.keys())]
    
    scaled_dict = {key: (value - X[key].min()) / (X[key].max() - X[key].min()) for key, value in input_dict.items()}
    return scaled_dict

def add_predictions(input_data):
    """Load model, scaler, and label encoder, predict and display crop recommendation."""
    try:
        model = pickle.load(open("C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/models/crop_recommendation_model.pkl", "rb"))
        scaler = pickle.load(open("C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/models/crop_recommendation_scaler.pkl", "rb"))
        label_encoder = pickle.load(open("C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/models/crop_recommendation_label_encoder.pkl", "rb"))
        
        input_df = pd.DataFrame([input_data], columns=input_data.keys())
        input_array_scaled = scaler.transform(input_df)
        
        prediction = model.predict(input_array_scaled)
        predicted_crop = label_encoder.inverse_transform(prediction)[0]
        
        st.subheader("Recommended Crop")
        st.write(f"Based on the input conditions, the recommended crop is **{predicted_crop}**.")
        
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")

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
        bar_chart = get_bar_chart(input_data)
        st.plotly_chart(bar_chart, use_container_width=True)
    with col2:
        add_predictions(input_data)

if __name__ == "__main__":
    main()
