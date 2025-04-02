import streamlit as st
import pandas as pd
import plotly.express as px
import re
import numpy as np

# Load dataset
file_path = "Mean Temperature Data (1).csv"
df = pd.read_csv(file_path)

# Melt data for better visualization
df_melted = df.melt(id_vars=["States", "Period"], var_name="Year", value_name="Temperature")
df_melted["Year"] = df_melted["Year"].astype(int)

# Streamlit UI
st.set_page_config(layout="wide", page_title="Climate Change Dashboard")
st.title("India Climate Change Data Visualization")

# Sidebar filters
selected_state = st.sidebar.selectbox("Select State", df["States"].unique())
selected_period = st.sidebar.selectbox("Select Period", df["Period"].unique())
year_range = st.sidebar.selectbox("Select Year Range", ["Every Year", "5 Years", "10 Years"])

# Text input for command-based queries
user_query = st.text_input("Enter your query (e.g., 'What if climate change in summer in Goa' or 'What if climate change in June in Maharashtra'):")

# Process user query dynamically
month_map = {"summer": "May", "winter": "Jan", "monsoon": "Sep", "spring": "Mar", "autumn": "Oct"}
months = {"january": "Jan", "february": "Feb", "march": "Mar", "april": "Apr", "may": "May", "june": "Jun", "july": "Jul", "august": "Aug", "september": "Sep", "october": "Oct", "november": "Nov", "december": "Dec"}

if user_query:
    user_query = user_query.lower()
    for season, month in month_map.items():
        if re.search(fr"\b{season}\b", user_query):
            selected_period = month
            break
    for month, abbr in months.items():
        if re.search(fr"\b{month}\b", user_query):
            selected_period = abbr
            break
    for state in df["States"].unique():
        if state.lower() in user_query:
            selected_state = state
            break

# Filter data based on selection
state_data = df_melted[(df_melted["States"] == selected_state) & (df_melted["Period"] == selected_period)]
if year_range == "5 Years":
    state_data = state_data[state_data["Year"] % 5 == 0]
elif year_range == "10 Years":
    state_data = state_data[state_data["Year"] % 10 == 0]

# Line chart: Climate change over years for selected state
fig1 = px.line(state_data, x="Year", y="Temperature", title=f"Temperature Trend in {selected_state} ({selected_period})",
               labels={"Temperature": "Mean Temperature (°C)", "Year": "Year"}, template="plotly_white")
st.plotly_chart(fig1, use_container_width=True)

# Climate change in 10-year intervals
df_melted["Decade"] = (df_melted["Year"] // 10) * 10
decade_avg = df_melted.groupby(["Decade", "States"])["Temperature"].mean().reset_index()
fig2 = px.line(decade_avg[decade_avg["States"] == selected_state], x="Decade", y="Temperature",
               title=f"Decadal Temperature Trend in {selected_state}", labels={"Temperature": "Mean Temperature (°C)"},
               template="plotly_white")
st.plotly_chart(fig2, use_container_width=True)

# State-wise comparison
state_avg = df_melted.groupby(["States", "Year"])["Temperature"].mean().reset_index()
fig3 = px.line(state_avg, x="Year", y="Temperature", color="States", title="State-wise Temperature Comparison Over Time",
               labels={"Temperature": "Mean Temperature (°C)", "Year": "Year"}, template="plotly_white")
st.plotly_chart(fig3, use_container_width=True)

# Overall India climate change trend
overall_data = df_melted.groupby("Year")["Temperature"].mean().reset_index()
fig4 = px.line(overall_data, x="Year", y="Temperature", title="Overall Temperature Trend in India",
               labels={"Temperature": "Mean Temperature (°C)", "Year": "Year"}, template="plotly_white")
st.plotly_chart(fig4, use_container_width=True)

# Additional heatmap
heatmap_data = df.pivot_table(index="States", columns="Period", values="2020")
fig5 = px.imshow(heatmap_data, labels=dict(color="Temperature (°C)"), title="State-wise Temperature for 2020",
                 color_continuous_scale="thermal", height=1000, width=1400)
st.plotly_chart(fig5, use_container_width=True)
