import streamlit as st
import requests
import pandas as pd
import numpy as np

# Page config
st.set_page_config(
    page_title="California House Price Predictor",
    page_icon="🏠",
    layout="wide"
)

# Input fields
# 📍 Location
longitude = st.slider("longitude", -125.0, -114.0, -122.23)
latitude = st.slider("latitude", 32.0, 42.0, 37.88)

# 🏠 House details
housing_median_age = st.slider("Housing Median Age (years)", 1, 52, 20)
total_rooms = st.number_input("Total Rooms", min_value=1, max_value=40000, value=1500)
total_bedrooms = st.number_input("Total Bedrooms", min_value=1, max_value=6000, value=300)

# 👨‍👩‍👧 Population & households
population = st.number_input("Population", min_value=1, max_value=35000, value=1000)
households = st.number_input("Households", min_value=1, max_value=6000, value=300)

# 💵 Income
median_income = st.slider("Median Income ($10k)", 0.5, 15.0, 5.0)

# 🌊 Ocean proximity
ocean_proximity = st.selectbox(
    "Ocean Proximity",
    ["INLAND", "NEAR BAY", "NEAR OCEAN", "ISLAND"]
    )


# Predict button
if st.button("Predict Price"):
    # Send data to FastAPI
    data = {
        "longitude": longitude,
        "latitude": latitude,
        "housing_median_age": housing_median_age,
        "total_rooms": total_rooms,
        "total_bedrooms": total_bedrooms,
        "population": population,
        "households": households,
        "median_income": median_income,
        "ocean_proximity": ocean_proximity 
    }
    #yocean_proximity = st.selectbox("Ocean Proximity", ["INLAND", "NEAR BAY", "NEAR OCEAN", "ISLAND"])

    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=data)
        result = response.json()
        price = result["predicted_median_house_value"]
        st.success(f"### Predicted Price: ${price:,.2f}")
    except:
        st.error("❌ Can't connect to the model. Is the API running?")


       