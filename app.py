import streamlit as st
import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
import requests  # <-- for live weather data

# Load Trained Model
model = joblib.load("traffic_random_forest_model_fixed.pkl")

st.set_page_config(page_title="Traffic Prediction", page_icon="🚦", layout="wide")

st.title("🚦 Traffic Situation Predictor")
st.markdown("""
This app predicts **traffic situations** based on date, time, and vehicle counts.
Now enhanced with **live weather insights** for smarter predictions 🌦️
""")
st.markdown("---")


st.subheader("🌤️ Live Weather Info")
city = st.text_input("Enter City Name", "Pune")

# Function to fetch weather
def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        res = requests.get(url)
        data = res.json()
        if res.status_code == 200:
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            condition = data["weather"][0]["main"]
            return temp, humidity, condition
        else:
            return None, None, None
    except:
        return None, None, None


api_key = st.secrets["api_key"]
temp, humidity, condition = get_weather(city, api_key)

if temp is not None:
    st.write(f"**Condition:** {condition}")
    st.write(f"**Temperature:** {temp}°C")
    st.write(f"**Humidity:** {humidity}%")
else:
    st.warning("Unable to fetch weather data. Please check city name or API key.")

st.markdown("---")

#  USER INPUT SECTION 
st.subheader("🕒 Time and Date Details")
col1, col2, col3 = st.columns(3)

with col1:
    hour_input = st.number_input("Enter Hour (1–12)", min_value=1, max_value=12, value=8)
with col2:
    am_pm = st.selectbox("Select AM/PM", ["AM", "PM"])
with col3:
    date_input = st.number_input("Date (1–31)", min_value=1, max_value=31, value=1)

day_input = st.selectbox(
    "Day of the Week",
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
)

# Convert to 24-hour format
if am_pm == "PM" and hour_input != 12:
    time_24 = hour_input + 12
elif am_pm == "AM" and hour_input == 12:
    time_24 = 0
else:
    time_24 = hour_input

# Vehicle inputs
st.markdown("### 🚗 Vehicle Count Inputs")
col4, col5, col6, col7 = st.columns(4)

with col4:
    car = st.number_input("Car Count", min_value=0)
with col5:
    bike = st.number_input("Bike Count", min_value=0)
with col6:
    bus = st.number_input("Bus Count", min_value=0)
with col7:
    truck = st.number_input("Truck Count", min_value=0)

total = car + bike + bus + truck
st.metric(label="Total Vehicles", value=total)

# Time Interval Encoding
def get_time_interval(hour_24):
    if 6 <= hour_24 < 10:
        return "Morning"
    elif 10 <= hour_24 < 16:
        return "Noon"
    elif 16 <= hour_24 < 21:
        return "Evening"
    else:
        return "Night"

interval = get_time_interval(time_24)
interval_map = {"Morning": 1, "Noon": 2, "Evening": 3, "Night": 4}
interval_encoded = interval_map[interval]

day_map = {
    "Monday": 1, "Tuesday": 2, "Wednesday": 3,
    "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7
}

# Prepare input
input_data = pd.DataFrame([[
    time_24,
    date_input,
    day_map[day_input],
    car,
    bike,
    bus,
    truck,
    interval_encoded
]], columns=["Time", "Date", "Day of the week", "CarCount", "BikeCount",
             "BusCount", "TruckCount", "Time Interval Encoded"])


st.markdown("---")
if st.button("🚦 Predict Traffic Situation"):
    input_data = input_data[model.feature_names_in_]
    pred = model.predict(input_data)[0]

    st.subheader("Prediction Result")
    if pred == 0:
        st.success("✅ **Traffic Situation: LOW** — Roads are clear! 🟢")
    elif pred == 1:
        st.warning("⚠️ **Traffic Situation: NORMAL** — Expect moderate flow. 🟡")
    else:
        st.error("🚨 **Traffic Situation: HEAVY** — High congestion ahead! 🔴")

   
    if temp is not None:
        st.markdown("### 🌦️ Weather Advisory:")
        if condition.lower() in ["rain", "thunderstorm", "drizzle"]:
            st.warning("⚠️ Rainy conditions — expect slower traffic and possible congestion.")
        elif condition.lower() in ["clear"]:
            st.info("🌞 Clear weather — smoother traffic expected.")
        elif condition.lower() in ["fog", "mist", "haze"]:
            st.warning("🌫️ Low visibility — drive carefully.")
        elif temp > 35:
            st.warning("🥵 High temperature — expect road heat and possible slowdown.")
        elif humidity > 80:
            st.info("💧 High humidity — slight risk of mist or reduced visibility.")
    else:
        st.info("Weather context unavailable — prediction based only on traffic data.")
