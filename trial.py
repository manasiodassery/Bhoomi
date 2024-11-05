import streamlit as st
import json

# Load schemes data from JSON file
def load_schemes_data():
    with open(r'C:\Manasi\NMIMS\Manasi\Capstone Project\Agriculture\Bhoomi\JSON files\schemes.json', 'r') as file:
        schemes = json.load(file)
    return schemes

# Streamlit app interface
st.set_page_config(page_title="Bhoomi: Government Schemes and Subsidies", page_icon="🌾", layout="centered")
st.title("Bhoomi: Government Schemes and Subsidies")
st.markdown("Explore various agricultural schemes and subsidies available for farmers.")

# Load schemes data
schemes = load_schemes_data()

# Search functionality
search_query = st.text_input("Search for a scheme or subsidy", "")

# Filter schemes based on search query
filtered_schemes = [
    scheme for scheme in schemes 
    if search_query.lower() in scheme.get('scheme_name', '').lower()
]

# Display schemes
if filtered_schemes:
    for scheme in filtered_schemes:
        with st.expander(scheme.get('scheme_name', 'Unknown Scheme')):
            st.write(f"**Description:** {scheme.get('description', 'N/A')}")
            st.write(f"**Eligibility:** {scheme.get('eligibility', 'N/A')}")
            st.write(f"**Benefits:** {scheme.get('benefits', 'N/A')}")
            st.write(f"**Application Process:** {scheme.get('application_process', 'N/A')}")
            st.write(f"[Official Link]({scheme.get('official_link', '#')})")
else:
    st.info("No schemes found. Please enter a different search term.")
 