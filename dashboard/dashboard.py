import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_data, kpi_calculations
import random

# Set up the page configuration
st.set_page_config(page_title="Weather Dashboard 🌤️", page_icon="🌤️", layout="wide")

# Load data
df = get_data()

# KPI Calculations
kpi = kpi_calculations(df)

# Helper function to display KPI metrics
def display_kpi(title, value):
    st.markdown(f"""
    <div style='text-align: center; background-color: #DBE2EF; border-radius: 10px; padding: 20px; height: 120px; display: flex; flex-direction: column; justify-content: center; align-items: center;'>
        <h2 style='color: #112D4E; margin: 0; font-size: 1.5em;'>{title}</h2>
        <h3 style='color: #3F72AF; margin: 0; font-size: 1.2em;'>{value}</h3>
    </div>
    """, unsafe_allow_html=True)

# Navigation Panel
menu = ["Home", "History", "Analytics", "About"]
choice = st.sidebar.selectbox("Menu", menu)

# Styling for entire app
st.markdown(
    """
    <style>
    .main {
        background-color: #F9F7F7;
    }
    h1 {
        color: #3F72AF;
    }
    h2, h3, h4 {
        color: #112D4E;
    }
    .streamlit-table {
        background-color: #FFE3E1;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Home Page
if choice == "Home":
    st.title("Weather Dashboard 🌤️")
    st.markdown("<h4 style='text-align: center; color: #3F72AF;'>Key Performance Indicators (KPIs)</h4>", unsafe_allow_html=True)

    # KPI Metrics in Horizontal Layout
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        display_kpi("Average Temperature", f"{kpi['avg_temp']:.2f} °C")
    with col2:
        display_kpi("Average Humidity", f"{kpi['avg_humidity']:.2f} %")
    with col3:
        display_kpi("Max Wind Speed", f"{kpi['max_wind_speed']:.2f} m/s")
    with col4:
        display_kpi("Total Cities", kpi['total_cities'])

    # Latest Data
    st.markdown("<h4 style='text-align: center; color: #3F72AF;'>Latest Weather Data</h4>", unsafe_allow_html=True)
    st.dataframe(df.tail(10).style.highlight_max(axis=0).set_table_attributes('class="streamlit-table"'))

# History Page
elif choice == "History":
    st.title("Historical Weather Data 📜")
    st.markdown("### Browse and Filter Historical Data")
    
    # Filter by City
    city_list = df['city'].unique().tolist()
    selected_city = st.selectbox("Select City", city_list)
    
    city_data = df[df['city'] == selected_city]
    st.write(f"Showing data for **{selected_city}**", unsafe_allow_html=True)
    st.dataframe(city_data.style.highlight_max(axis=0).set_table_attributes('class="streamlit-table"'))

# Analytics Page
elif choice == "Analytics":
    st.title("Weather Analytics 📊")
    st.markdown("### Visualize Weather Trends and Insights")

    # Line Chart: Temperature Trend
    st.markdown("#### Temperature Trend")
    temperature_fig = px.line(df, x="timestamp", y="temperature", 
                               title='Temperature Trend Over Time',
                               line_shape='linear',
                               template='plotly',
                               color_discrete_sequence=["#FF6F61"])  # Custom color
    st.plotly_chart(temperature_fig, use_container_width=True)

    # Bar Chart: Average Humidity by City
    st.markdown("#### Average Humidity by City")
    avg_humidity_city = df.groupby("city")['humidity'].mean().sort_values(ascending=False)
    
    # Generate random colors for each city
    colors = ["#FF6F61", "#6B5B93", "#88B04B", "#F7CAC9", "#92A8D1", "#955251", "#B5E61D", "#D5B07A"]
    random.shuffle(colors)  # Shuffle colors for variety
    humidity_fig = px.bar(avg_humidity_city, title='Average Humidity by City', 
                           labels={'x': 'City', 'y': 'Humidity (%)'},
                           color=avg_humidity_city.index,
                           color_discrete_sequence=colors)  # Assign random colors
    st.plotly_chart(humidity_fig, use_container_width=True)

    # Wind Speed Distribution with Plotly
    st.markdown("#### Wind Speed Distribution")
    fig = px.histogram(df, x="wind_speed", nbins=20, 
                        labels={'wind_speed': 'Wind Speed (m/s)'}, 
                        title='Wind Speed Distribution',
                        hover_data=['wind_speed'],
                        color_discrete_sequence=["#FF5733"])  # Menggunakan warna mencolok
    st.plotly_chart(fig, use_container_width=True)

# About Page
elif choice == "About":
    st.title("Tentang Dashboard Ini ℹ️")
    st.markdown("""
    Dashboard cuaca ini dibangun menggunakan **Streamlit**.  
    Ini memungkinkan pengguna untuk menjelajahi data cuaca, melacak metrik utama, dan memvisualisasikan tren.
    
    **Pengembang:**
    - Dea Kayla P. D. (3323600005)
    - Dinda Ayu P. (3323600012)

    **Alat:**
    - Python, Streamlit, Docker, Git, Airflow

    **Kontak:**
    - Email:
      - deakayla10@gmail.com
      - dindapermatasri020@gmail.com
    - GitHub: [GitHub Profile](https://github.com/dindaapermatasari/weather-monitoring)

    """)

# Footer
st.markdown("---")
st.markdown("© 2024 Weather Dashboard. All rights reserved.")