import streamlit as st
import pandas as pd
import os


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="EV Charge Intelligence",
    page_icon="⚡",
    layout="wide"
)


# --------------------------------------------------
# Load analytics data
# --------------------------------------------------

BASE_PATH = "data/analytics"


@st.cache_data
def load_data():
    hourly = pd.read_csv(
        os.path.join(BASE_PATH, "hourly_metrics.csv")
    )

    daily = pd.read_csv(
        os.path.join(BASE_PATH, "daily_metrics.csv")
    )

    location = pd.read_csv(
        os.path.join(BASE_PATH, "location_metrics.csv")
    )

    charger = pd.read_csv(
        os.path.join(BASE_PATH, "charger_metrics.csv")
    )

    user = pd.read_csv(
        os.path.join(BASE_PATH, "user_metrics.csv")
    )

    peak = pd.read_csv(
        os.path.join(BASE_PATH, "peak_hour_metrics.csv")
    )

    monthly = pd.read_csv(
        os.path.join(BASE_PATH, "monthly_metrics.csv")
    )

    return (
        hourly,
        daily,
        location,
        charger,
        user,
        peak,
        monthly
    )


(
    hourly,
    daily,
    location,
    charger,
    user,
    peak,
    monthly
) = load_data()


# --------------------------------------------------
# Prepare monthly labels
# --------------------------------------------------

monthly["MonthLabel"] = (
    monthly["Year"].astype(str)
    + "-"
    + monthly["Month"].astype(str).str.zfill(2)
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("EV Charge Intelligence")

st.write(
    "Interactive analytics dashboard for EV charging sessions, "
    "demand, locations, chargers, users, and charging trends."
)


# --------------------------------------------------
# KPI calculations
# --------------------------------------------------

total_sessions = int(location["Sessions"].sum())

total_demand = location["TotalDemand"].sum()

total_users = int(user["UserID"].nunique())

total_chargers = int(charger["ChargerID"].nunique())

total_locations = int(location["Location"].nunique())

average_demand = location["TotalDemand"].sum() / location["Sessions"].sum()


# --------------------------------------------------
# KPI cards
# --------------------------------------------------

st.subheader("Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Sessions",
    f"{total_sessions:,}"
)

col2.metric(
    "Total Demand",
    f"{total_demand:,.1f} kWh"
)

col3.metric(
    "Users",
    f"{total_users:,}"
)

col4.metric(
    "Chargers",
    f"{total_chargers:,}"
)

col5.metric(
    "Locations",
    f"{total_locations:,}"
)


st.divider()


# --------------------------------------------------
# Hourly analysis
# --------------------------------------------------

st.subheader("Charging Activity by Hour")

col1, col2 = st.columns(2)

with col1:

    st.write("Sessions by Hour")

    hourly_chart = hourly.set_index("StartHour")["Sessions"]

    st.bar_chart(hourly_chart)


with col2:

    st.write("Demand by Hour")

    hourly_demand_chart = hourly.set_index(
        "StartHour"
    )["TotalDemand"]

    st.line_chart(hourly_demand_chart)


# --------------------------------------------------
# Location analysis
# --------------------------------------------------

st.subheader("Charging Demand by Location")

location_chart = location.sort_values(
    "TotalDemand",
    ascending=False
)

st.bar_chart(
    location_chart.set_index("Location")["TotalDemand"]
)


# --------------------------------------------------
# Location table
# --------------------------------------------------

st.write("Location Performance")

location_display = location.sort_values(
    "TotalDemand",
    ascending=False
)[
    [
        "Location",
        "Sessions",
        "TotalDemand",
        "AverageDemand",
        "AverageDuration",
        "UniqueUsers",
        "ActiveChargers"
    ]
]

st.dataframe(
    location_display,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# Monthly trend
# --------------------------------------------------

st.subheader("Monthly Charging Trend")

monthly_chart = monthly.set_index(
    "MonthLabel"
)["TotalDemand"]

st.line_chart(monthly_chart)


# --------------------------------------------------
# Peak vs non-peak
# --------------------------------------------------

st.subheader("Peak vs Non-Peak Charging")

col1, col2 = st.columns(2)

with col1:

    st.write("Sessions")

    peak_sessions = peak.set_index(
        "Period"
    )["Sessions"]

    st.bar_chart(peak_sessions)


with col2:

    st.write("Average Demand")

    peak_demand = peak.set_index(
        "Period"
    )["AverageDemand"]

    st.bar_chart(peak_demand)


# --------------------------------------------------
# Charger analysis
# --------------------------------------------------

st.subheader("Top Chargers")

top_chargers = charger.sort_values(
    "Sessions",
    ascending=False
).head(10)

st.dataframe(
    top_chargers[
        [
            "ChargerID",
            "Sessions",
            "TotalDemand",
            "AverageDemand",
            "AverageDuration",
            "UniqueUsers",
            "Location",
            "ChargerCompany",
            "ChargerType"
        ]
    ],
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# User analysis
# --------------------------------------------------

st.subheader("Top Users")

top_users = user.sort_values(
    "Sessions",
    ascending=False
).head(10)

st.dataframe(
    top_users[
        [
            "UserID",
            "Sessions",
            "TotalDemand",
            "AverageDemand",
            "AverageDuration",
            "UniqueChargers",
            "UniqueLocations"
        ]
    ],
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# Business insights
# --------------------------------------------------

st.subheader("Business Insights")

busiest_hour = hourly.loc[
    hourly["Sessions"].idxmax()
]

highest_demand_location = location.loc[
    location["TotalDemand"].idxmax()
]

highest_demand_month = monthly.loc[
    monthly["TotalDemand"].idxmax()
]

peak_period = peak.loc[
    peak["Period"] == "Peak Hour"
]

col1, col2, col3 = st.columns(3)

with col1:

    st.write("Busiest Hour")

    st.metric(
        "Charging Sessions",
        f"{int(busiest_hour['Sessions']):,}",
        f"{int(busiest_hour['StartHour'])}:00"
    )


with col2:

    st.write("Highest Demand Location")

    st.metric(
        "Total Demand",
        f"{highest_demand_location['TotalDemand']:,.2f} kWh",
        highest_demand_location["Location"]
    )


with col3:

    st.write("Highest Demand Month")

    st.metric(
        "Total Demand",
        f"{highest_demand_month['TotalDemand']:,.2f} kWh",
        highest_demand_month["MonthLabel"]
    )


# --------------------------------------------------
# Peak insight
# --------------------------------------------------

if not peak_period.empty:

    st.info(
        f"Peak hours recorded "
        f"{int(peak_period.iloc[0]['Sessions']):,} sessions "
        f"with an average demand of "
        f"{peak_period.iloc[0]['AverageDemand']:.2f} kWh "
        f"per session."
    )


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "EV Charge Intelligence | "
    "Python | Pandas | Matplotlib | Streamlit | Git/GitHub"
)