import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
import requests
import asyncio
import aiohttp
import plotly.io as pio

st.set_page_config(
    page_title="Claim Leakage Dashboard Testing",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        /* General body background color */
        body {
            background-color: #f0f0f0;
        }
        /* Sidebar custom styling */
        .sidebar .sidebar-content {
            background-color: #ffffff;
        }
        /* Input fields in sidebar */
        .css-1to6prn input {
            border: 2px solid #5d3a9b;
            background-color: #f8f8f8;
            color: #333333;
            padding: 10px;
        }
        /* Sidebar header styling */
        .css-1to6prn label {
            color: #5d3a9b;
        }
        /* Title and Subheader text color */
        .css-ffhzg2 {
            color: #5d3a9b;
        }
        /* Button Styling */
        .css-1v3fvcr button {
            background-color: #5d3a9b;
            color: white;
            border-radius: 5px;
        }
        /* Styling for Metric Cards */
        .css-1v3fvcr {
            background-color: #5d3a9b;
            color: white;
            border-radius: 5px;
        }
        /* Change background of the filters */
        .stTextInput {
            background-color: #e0e0e0;
            border-radius: 8px;
            padding: 10px;
            border: 2px solid #5d3a9b;
        }
        /* Metric card styling */
        .stMetric {
            background-color: #ffffff;
            border: 2px solid #5d3a9b;
            padding: 15px;
            border-radius: 8px;
        }
        /* Styling for the multiselect input */
        .stMultiSelect {
            background-color: #e0e0e0;
            border-radius: 8px;
            padding: 10px;
            border: 2px solid #5d3a9b;
        }
        /* Change text color and border of selected items */
        .stMultiSelect input {
            color: #5d3a9b;
            background-color: #f8f8f8;
            padding: 8px;
        }
        /* Styling for the dropdown options */
        div[role="listbox"] {
            background-color: #f8f8f8; /* Background color of the dropdown */
            border: 2px solid #5d3a9b; /* Border color of the dropdown */
            border-radius: 8px;
            padding: 8px;
        }
        /* Change selected option in the dropdown */
        div[role="option"][aria-selected="true"] {
            background-color: #5d3a9b; /* Background color when an option is selected */
            color: white; /* Text color of the selected option */
        }
        /* Optional: Change unselected options background color */
        div[role="option"]:not([aria-selected="true"]) {
            background-color: #e0e0e0; /* Light gray for unselected options */
            color: #5d3a9b; /* Border color for unselected options */
        }
        /* Styling for the multiselect input */
        .stDateInput {
            background-color: #e0e0e0;
            border-radius: 8px;
            padding: 10px;
            border: 2px solid #5d3a9b;
        }
        /* Change text color, background color, and border of the selected item */
        .stDateInput input {
            color: #5d3a9b; /* Text color same as border color */
            background-color: #f8f8f8;
            padding: 8px;
        }
        .stDateInput input::placeholder {
            color: #5d3a9b; /* Match placeholder text color with the border */
        }
    </style>
""", unsafe_allow_html=True)

async def fetch_data():
    url = "http://localhost:8000/api/fetch_claims_data/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def fetch_graphs():
    url = "http://localhost:8000/api/generate_graphs/"
    response = requests.get(url)
    return response.json()

async def dashboard1():
    st.image("exl.png", width=150)
    st.title("Claim Report Dashboard Testing")

    # Sidebar for filters
    st.sidebar.header("Filter Options")

    claim_numbers = st.sidebar.text_input("Filter by Claim Number (comma-separated)")
    source_system = st.sidebar.multiselect("Filter by Source System", options=["All", "System1", "System2"], default=["All"])
    general_nature_of_loss = st.sidebar.multiselect("Filter by General Nature of Loss", options=["All", "Loss1", "Loss2"], default=["All"])
    line_of_business = st.sidebar.multiselect("Filter by Line of Business", options=["All", "Business1", "Business2"], default=["All"])
    claim_status = st.sidebar.multiselect("Filter by Claim Status", options=["All", "Status1", "Status2"], default=["All"])
    fault_rating = st.sidebar.multiselect("Filter by Fault Rating", options=["All", "Rating1", "Rating2"], default=["All"])
    fault_categorisation = st.sidebar.multiselect("Filter by Fault Categorisation", options=["All", "Category1", "Category2"], default=["All"])

    date_columns = [
        'claim_received_date', 'claim_loss_date', 'claim_finalised_date',
        'original_verified_date_of_loss_time', 'last_verified_date_of_loss_time',
        'catastrophe_valid_from_date_time', 'catastrophe_valid_to_date_time'
    ]
    date_filters = {}
    for col in date_columns:
        date_range = st.sidebar.date_input(f"{col} Range", value=(datetime(2020, 1, 1), datetime(2023, 1, 1)))
        date_filters[f"{col}_start"] = date_range[0]
        date_filters[f"{col}_end"] = date_range[1]

    params = {
        # Add your parameters here
    }

    graphs = await fetch_graphs()

    if graphs:
        st.subheader("Graphs")
        fig_status = pio.from_json(graphs['fig_status_json'])
        st.plotly_chart(fig_status)

        fig_time = pio.from_json(graphs['fig_time_json'])
        st.plotly_chart(fig_time)

        fig_pie = pio.from_json(graphs['fig_pie_json'])
        st.plotly_chart(fig_pie)

        fig_line_of_business = pio.from_json(graphs['fig_line_of_business_json'])
        st.plotly_chart(fig_line_of_business)

        fig_trend_monthly = pio.from_json(graphs['fig_trend_monthly_json'])
        st.plotly_chart(fig_trend_monthly)
    else:
        st.warning("No data available.")

async def dashboard2():
    st.image("exl.png", width=150)
    st.title("Claim Report Dashboard Testing")

    # Sidebar for filters
    st.sidebar.header("Filter Options")

    claim_numbers = st.sidebar.text_input("Filter by Claim Number (comma-separated)")
    source_system = st.sidebar.multiselect("Filter by Source System", options=["All", "System1", "System2"], default=["All"])
    general_nature_of_loss = st.sidebar.multiselect("Filter by General Nature of Loss", options=["All", "Loss1", "Loss2"], default=["All"])
    line_of_business = st.sidebar.multiselect("Filter by Line of Business", options=["All", "Business1", "Business2"], default=["All"])
    claim_status = st.sidebar.multiselect("Filter by Claim Status", options=["All", "Status1", "Status2"], default=["All"])
    fault_rating = st.sidebar.multiselect("Filter by Fault Rating", options=["All", "Rating1", "Rating2"], default=["All"])
    fault_categorisation = st.sidebar.multiselect("Filter by Fault Categorisation", options=["All", "Category1", "Category2"], default=["All"])

    date_columns = [
        'claim_received_date', 'claim_loss_date', 'claim_finalised_date',
        'original_verified_date_of_loss_time', 'last_verified_date_of_loss_time',
        'catastrophe_valid_from_date_time', 'catastrophe_valid_to_date_time'
    ]
    date_filters = {}
    for col in date_columns:
        date_range = st.sidebar.date_input(f"{col} Range", value=(datetime(2020, 1, 1), datetime(2023, 1, 1)))
        date_filters[f"{col}_start"] = date_range[0]
        date_filters[f"{col}_end"] = date_range[1]

    params = {
        # Add your parameters here
    }

    data = await fetch_data()

    if data:
        st.subheader("Filtered Claims Statistics")
        st.write("Total Claims:", data["total_claims"])

        st.subheader("Metrics Overview")
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            st.metric("Claims Monitored", data["claims_monitored"])
        with col2:
            st.metric("Claims with Leakage Opportunity", data["claims_with_leakage_opportunity"])
        with col3:
            st.metric("Leakage Opportunity %", data["leakage_opportunity_percentage"])
        with col4:
            st.metric("Potential Leakage $", f"${data['potential_leakage']:,}")
        with col5:
            st.metric("Leakage Rate %", data["leakage_rate_percentage"])
        with col6:
            st.metric("Opportunities Not Actioned", data["opportunities_not_actioned"])

        col1, col2 = st.columns(2, gap="small")

        with col1:
            st.subheader("Claims by Status")
            status_counts = pd.DataFrame(data["status_counts"])
            fig_status = px.bar(status_counts, x='claim_status', y='count', title="Claims by Status", color='claim_status')
            st.plotly_chart(fig_status)

        with col2:
            st.subheader("Claims Over Time")
            claims_over_time = pd.DataFrame(data["claims_over_time"])
            fig_time = px.line(claims_over_time, x='claim_received_date', y='claim_count', title="Claims Over Time")
            st.plotly_chart(fig_time)

        col3, col4 = st.columns(2, gap="small")

        with col3:
            st.subheader("Claim Status Distribution")
            fig_pie = px.pie(status_counts, names='claim_status', title="Claim Status Distribution", hole=0.3)
            st.plotly_chart(fig_pie)

        with col4:
            st.subheader("Claims by Line of Business")
            line_of_business_counts = pd.DataFrame(data["line_of_business_counts"])
            fig_line_of_business = px.bar(line_of_business_counts, y='line_of_business', x='count', orientation='h', title="Claims by Line of Business")
            st.plotly_chart(fig_line_of_business)

        st.subheader("Claim Status Trend Over Months")
        monthly_status_counts = pd.DataFrame(data["monthly_status_counts"])
        fig_trend_monthly = px.bar(monthly_status_counts, x='month_year', y='count', color='claim_status', title="Monthly Claim Status Trend (Open vs Closed)", barmode='group')
        st.plotly_chart(fig_trend_monthly)

        st.subheader("Filtered Claims Data")
        filtered_data = pd.DataFrame(data["filtered_data"])
        st.dataframe(filtered_data)

        csv = filtered_data.to_csv(index=False)
        st.download_button("Download as CSV", csv, "filtered_claims.csv", "text/csv")
    else:
        st.warning("No data available.")

async def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard 1", "Dashboard 2"])

    if page == "Dashboard 1":
        await dashboard1()
    elif page == "Dashboard 2":
        await dashboard2()

if __name__ == "__main__":
    asyncio.run(main())