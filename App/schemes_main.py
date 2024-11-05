import streamlit as st
import json

# Load schemes data from JSON file
def load_schemes_data():
    with open(r'C:\Manasi\NMIMS\Manasi\Capstone Project\Agriculture\Bhoomi\JSON files\schemes.json', 'r') as file:
        schemes = json.load(file)
    return schemes

# Streamlit app interface
st.set_page_config(page_title="Bhoomi: Government Schemes and Subsidies", page_icon="🌾", layout="wide")
st.title("Bhoomi: Government Schemes and Subsidies")
st.markdown("Find various government schemes and subsidies available to support farmers.")

# Load schemes data
schemes = load_schemes_data()

# Sidebar search input
st.sidebar.header("Search Schemes")
search_query = st.sidebar.text_input("Enter scheme name or keyword", "")

# Filter schemes based on search query
filtered_schemes = {
    name: details for name, details in schemes.items() 
    if search_query.lower() in name.lower()
}

# Display filtered schemes
st.subheader("Available Schemes")
if filtered_schemes:
    for scheme_name, details in filtered_schemes.items():
        with st.expander(scheme_name):
            st.write(f"**Introduction:** {details.get('Introduction', 'N/A')}")
            st.write(f"**Implementation Period:** {details.get('Implementation Period', 'N/A')}")
            st.write(f"**Budget:** {details.get('Budget', 'N/A')}")
            st.write(f"**Objective:** {details.get('Objective', 'N/A')}")
            st.write(f"**Eligibility:** {details.get('Eligibility', 'N/A')}")
            
            # Handle Benefits and Features as nested sections if present
            if "Benefits" in details:
                st.write("**Benefits:**")
                for benefit, description in details["Benefits"].items():
                    st.write(f"- **{benefit}:** {description}")
            if "Focus Areas" in details:
                st.write("**Focus Areas:**")
                for focus, description in details["Focus Areas"].items():
                    st.write(f"- **{focus}:** {description}")
            if "Services" in details:
                st.write("**Services:**")
                for service, description in details["Services"].items():
                    st.write(f"- **{service}:** {description}")
            if "Features" in details:
                st.write("**Features:**")
                for feature, description in details["Features"].items():
                    st.write(f"- **{feature}:** {description}")
                    
            st.write(f"[More Information]({details.get('More Information', '#')})")
else:
    st.info("No schemes found. Please enter a different search term.")
