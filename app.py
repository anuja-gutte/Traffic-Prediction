import streamlit as st
import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt


# Load Trained Model

model = joblib.load("traffic_random_forest_model_fixed.pkl")


# Page Configuration

st.set_page_config(page_title="Traffic Prediction", page_icon="🚦", layout="wide")

st.title("🚦Traffic Situation Predictor")
st.markdown("""
This app predicts **traffic situations** based on date, time, and vehicle counts.
Enter your inputs below to get real-time traffic insights.
""")

st.markdown("---")


# Input Section

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


# Convert time to 24-hour format
if am_pm == "PM" and hour_input != 12:
    time_24 = hour_input + 12
elif am_pm == "AM" and hour_input == 12:
    time_24 = 0
else:
    time_24 = hour_input


# Vehicle Count Inputs
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

# ---------------------
# Time Interval Encoding
# ---------------------
def get_time_interval(hour_24):
    """Convert 24-hour time to traffic time interval."""
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

# Encode Day of Week

day_map = {
    "Monday": 1, "Tuesday": 2, "Wednesday": 3,
    "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7
}


# Prepare Input Data

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



# Prediction Section

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

