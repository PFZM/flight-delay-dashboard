import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("data/flight_delays.csv")

st.set_page_config(page_title="Flight Delay Dashboard", layout="wide")
st.title("✈️ U.S. Flight Delay Dashboard")
st.markdown("Explore airline arrival delays by carrier and month. Data source: U.S. DOT")

# Sidebar filters
carriers = df['carrier_name'].unique()
selected_carrier = st.sidebar.selectbox("Select Carrier", sorted(carriers))

years = df['year'].unique()
selected_year = st.sidebar.selectbox("Select Year", sorted(years, reverse=True))

months = df['month'].unique()
selected_month = st.sidebar.selectbox("Select Month", sorted(months))

# Filtered dataset
filtered = df[
    (df['carrier_name'] == selected_carrier) &
    (df['year'] == selected_year) &
    (df['month'] == selected_month)
]

# Metrics display
st.subheader(f"Delay Summary - {selected_carrier}, {selected_year}-{selected_month:02d}")
if filtered.empty:
    st.warning("No data available for the selected filters.")
else:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Arrivals", int(filtered['arr_flights'].sum()))
    col2.metric("Delayed Flights (15+ mins)", int(filtered['arr_del15'].sum()))
    col3.metric("Total Delay (min)", int(filtered['arr_delay'].sum()))

    # Bar chart of delay causes
    delay_causes = {
        "Carrier Delay": filtered["carrier_delay"].sum(),
        "Weather Delay": filtered["weather_delay"].sum(),
        "NAS Delay": filtered["nas_delay"].sum(),
        "Security Delay": filtered["security_delay"].sum(),
        "Late Aircraft": filtered["late_aircraft_delay"].sum()
    }

    delay_df = pd.DataFrame(list(delay_causes.items()), columns=["Cause", "Minutes Delayed"])
    fig = px.bar(delay_df, x="Cause", y="Minutes Delayed",
                 title="Delay Causes Breakdown",
                 color="Cause", height=400)
    st.plotly_chart(fig, use_container_width=True)

# Raw data toggle
with st.expander("📄 Show Raw Data"):
    st.dataframe(filtered)
