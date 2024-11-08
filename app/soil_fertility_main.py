import streamlit as st
import pickle
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def get_clean_data(filepath="C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/Data/soil_fertility.csv"):
    return pd.read_csv(filepath)

def add_sidebar():
    st.sidebar.header("Soil Composition and Properties")
    data = get_clean_data()
    
    slider_labels = [
        ("Nitrogen (N)", "N"), ("Phosphorus (P)", "P"), ("Potassium (K)", "K"),
        ("pH Level", "pH"), ("Electrical Conductivity (EC)", "EC"),
        ("Organic Carbon (OC)", "OC"), ("Sulfur (S)", "S"), 
        ("Zinc (Zn)", "Zn"), ("Iron (Fe)", "Fe"),
        ("Copper (Cu)", "Cu"), ("Manganese (Mn)", "Mn"), ("Boron (B)", "B")
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
    """Generate a radar chart with multiple traces for different soil composition metrics."""
    input_data = get_scaled_values(input_data)
    categories = list(input_data.keys())

    fig = go.Figure()

    # Add trace for "Current Soil Composition"
    fig.add_trace(go.Scatterpolar(
        r=list(input_data.values()),
        theta=categories,
        fill='toself',
        name='Current Soil Composition'
    ))

    # Hypothetical "Optimal Soil Composition" for comparison
    optimal_values = [0.7, 0.6, 0.8, 0.5, 0.3, 0.7, 0.6, 0.4, 0.5, 0.2, 0.6, 0.3]  # Example values
    fig.add_trace(go.Scatterpolar(
        r=optimal_values,
        theta=categories,
        fill='toself',
        name='Optimal Soil Composition'
    ))

    # Hypothetical "Standard Range" trace for illustrative comparison
    standard_range_values = [0.5, 0.4, 0.6, 0.3, 0.2, 0.5, 0.4, 0.3, 0.4, 0.2, 0.5, 0.3]  # Example values
    fig.add_trace(go.Scatterpolar(
        r=standard_range_values,
        theta=categories,
        fill='toself',
        name='Standard Range'
    ))

    # Update layout for radar chart
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title="Soil Composition Radar Chart"
    )
    
    return fig

def add_predictions(input_data):
    """Load model and scaler, predict and display soil fertility classification."""
    try:
        # Load the model and scaler
        model = pickle.load(open("C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/models/soil_fertility_model.pkl", "rb"))
        scaler = pickle.load(open("C:/Manasi/NMIMS/Manasi/Capstone Project/Bhoomi/models/soil_fertility_scaler.pkl", "rb"))
        
        # Convert input data to DataFrame for scaler compatibility
        input_df = pd.DataFrame([input_data], columns=input_data.keys())
        input_array_scaled = scaler.transform(input_df)
        
        # Predict soil fertility
        prediction = model.predict(input_array_scaled)
        
        st.subheader("Soil Fertility Classification")
        
        # Display the classification directly if it's a label
        if isinstance(prediction[0], str):
            st.write(f"Based on the input conditions, the soil is classified as **{prediction[0]}**.")
        else:
            # If the model returns an integer, map it to the label
            classification = ["Less Fertile", "Fertile", "Highly Fertile"][int(prediction[0])]
            st.write(f"Based on the input conditions, the soil is classified as **{classification}**.")
        
    except (ValueError, IndexError, KeyError, TypeError) as e:
        st.error(f"An error occurred during prediction: {e}")
        st.write("Please ensure the model and scaler are correctly loaded and compatible with the input format.")

def main():
    st.set_page_config(
        page_title="Bhoomi: Soil Fertility Classifier",
        layout="wide",
        page_icon="🌱",
        initial_sidebar_state="expanded"
    )
    input_data = add_sidebar()

    with st.container():
        st.title("Bhoomi: Soil Fertility Classifier")
        st.write("Adjust the sliders to reflect the elemental composition of your soil sample and check its fertility level.")

    col1, col2 = st.columns([3, 1])
    with col1:
        radar_chart = get_radar_chart(input_data)
        st.plotly_chart(radar_chart, use_container_width=True)
    with col2:
        add_predictions(input_data)

if __name__ == "__main__":
    main()
