
import streamlit as st
import pandas as pd
import plotly.express as px

# ---- Set Page Config ----
st.set_page_config(page_title="UrbanTrack - Vehicle Dashboard", layout="wide")

# ---- Mock Data ----
vehicle_data = {
    "Fuel Remaining (L)": [20, 18, 15, 13, 10],
    "Distance Covered (km)": [50, 120, 190, 260, 330],
    "Fuel Used (L)": [5, 7, 8, 6, 7],
    "Trip Time (hrs)": [1, 2, 3, 4, 5],
    "Date": ["2024-12-23", "2024-12-24", "2024-12-25", "2024-12-26", "2024-12-27"]
}

# Create DataFrame
df = pd.DataFrame(vehicle_data)

# ---- Inject Custom CSS for Styling ----
st.markdown(
    """
    <style>
    /* Set background gradient color */
    .stApp {
        background: linear-gradient(135deg, #a1c4fd, #c2e9fb); /* Light blue gradient */
    }
    /* Customize title font style */
    h1 {
        font-family: 'Arial', sans-serif;
        font-size: 3.5em;
        color: #004080; /* Dark blue */
        text-align: center;
        margin-bottom: 30px;
        font-weight: bold;
    }
    h2, h3 {
        font-family: 'Arial', sans-serif;
        color: #004080; /* Dark blue */
    }
    /* Customization for Metric labels and values */
    .stMetric-label, .stMetric-value {
        font-family: 'Arial', sans-serif;
        font-size: 1.2em;
        color: #004080; /* Dark blue */
    }
    /* Grid Layout for Key Metrics */
    .stColumns > div {
        padding: 10px;
        text-align: center;
        border-radius: 8px;
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    /* Chart styling */
    .stPlotlyChart {
        border-radius: 8px;
        margin-top: 20px;
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    /* Styling for DataFrame */
    .stDataFrame table {
        font-family: 'Arial', sans-serif;
        color: #004080;
        border-collapse: collapse;
    }
    .stDataFrame td, .stDataFrame th {
        padding: 12px;
        border: 1px solid #dddddd;
        text-align: left;
    }
    /* Hover effect for DataFrame */
    .stDataFrame tr:hover {
        background-color: #f5f5f5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- Layout ----
st.title("🚗 Routellingent Dashboard 🚙")
st.markdown("Track key vehicle metrics, fuel usage, and travel trends in real-time.")

# ---- Key Performance Indicators (KPIs) ----
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Current Fuel Remaining", value=f"{vehicle_data['Fuel Remaining (L)'][-1]} L")
with col2:
    st.metric(label="Total Distance Covered", value=f"{sum(vehicle_data['Distance Covered (km)'])} km")
with col3:
    st.metric(label="Fuel Used Today", value=f"{vehicle_data['Fuel Used (L)'][-1]} L")

# ---- Performance Metrics Grid ----
st.markdown("## 📊 Performance Metrics Over Time")

# Create 2x2 grid layout
grid_col1, grid_col2 = st.columns(2)

with grid_col1:
    # Line Chart - Distance Covered
    fig_distance = px.line(
        df,
        x="Date",
        y="Distance Covered (km)",
        title="Distance Covered Over Time",
        markers=True
    )
    st.plotly_chart(fig_distance, use_container_width=True)

with grid_col2:
    # Bar Chart - Fuel Used
    fig_fuel = px.bar(
        df,
        x="Date",
        y="Fuel Used (L)",
        title="Fuel Usage Over Time",
        color="Fuel Used (L)"
    )
    st.plotly_chart(fig_fuel, use_container_width=True)

# ---- Fuel Remaining vs Used Pie Chart ----
st.markdown("### 🚦 Fuel Distribution")
fuel_data = {"Fuel Remaining": df["Fuel Remaining (L)"].iloc[-1], "Fuel Used": sum(df["Fuel Used (L)"])}
fig_pie = px.pie(
    names=list(fuel_data.keys()),
    values=list(fuel_data.values()),
    title="Fuel Remaining vs. Used"
)
st.plotly_chart(fig_pie, use_container_width=True)

# ---- Additional Details Grid Layout ----
st.markdown("### 📅 Detailed Trip Data")
st.dataframe(df)

# ---- Upcoming Distance Estimation ----
distance_left = 500 - sum(vehicle_data["Distance Covered (km)"])
st.info(f"The vehicle needs to travel **{distance_left} km** to complete the journey.")

# ---- Footer ----
st.markdown("Designed by Aditya. Powered by **Streamlit**.")
