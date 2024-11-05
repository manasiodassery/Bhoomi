import streamlit as st
import requests

# Function to fetch weather data
def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"]
        }
    else:
        return None

# Streamlit app interface
st.set_page_config(page_title="Bhoomi: Weather Forecasting", page_icon="🌦️", layout="wide")
st.title("Bhoomi: Weather Forecasting Tool")
st.markdown("Get real-time weather updates to make informed agricultural decisions.")

# Sidebar for location input
st.sidebar.header("Enter Location")
city = st.sidebar.text_input("Location", placeholder="e.g., Mumbai")

# API key
api_key = "6aaae7fd26b0b6de2301c0d68113a578"

# Display weather information
st.subheader("Weather Forecast")
if city:
    weather_data = get_weather(city, api_key)
    if weather_data:
        col1, col2 = st.columns([1, 3])

        # Display weather icon in the first column
        with col1:
            icon_url = f"http://openweathermap.org/img/wn/{weather_data['icon']}@2x.png"
            st.image(icon_url, width=100)

        # Display weather details in the second column
        with col2:
            st.markdown(f"### Weather in **{weather_data['city']}**")
            st.markdown(f"""
            - **Temperature:** {weather_data['temperature']} °C 🌡️
            - **Humidity:** {weather_data['humidity']}% 💧
            - **Condition:** {weather_data['description'].capitalize()} 🌤️
            """)
    else:
        st.error("Could not retrieve weather data. Please try again.")
else:
    st.info("Please enter a location in the sidebar to get weather updates.")
