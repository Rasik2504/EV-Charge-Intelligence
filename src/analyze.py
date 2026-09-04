import pandas as pd
import os


# --------------------------------------------------
# 1. Load analytics datasets
# --------------------------------------------------

base_path = "data/analytics"

hourly = pd.read_csv(os.path.join(base_path, "hourly_metrics.csv"))
daily = pd.read_csv(os.path.join(base_path, "daily_metrics.csv"))
location = pd.read_csv(os.path.join(base_path, "location_metrics.csv"))
charger = pd.read_csv(os.path.join(base_path, "charger_metrics.csv"))
user = pd.read_csv(os.path.join(base_path, "user_metrics.csv"))
peak = pd.read_csv(os.path.join(base_path, "peak_hour_metrics.csv"))
monthly = pd.read_csv(os.path.join(base_path, "monthly_metrics.csv"))


# --------------------------------------------------
# 2. Hourly charging insights
# --------------------------------------------------

busiest_hour = hourly.loc[hourly["Sessions"].idxmax()]
highest_demand_hour = hourly.loc[hourly["TotalDemand"].idxmax()]


# --------------------------------------------------
# 3. Location insights
# --------------------------------------------------

top_location = location.loc[location["Sessions"].idxmax()]
highest_demand_location = location.loc[location["TotalDemand"].idxmax()]


# --------------------------------------------------
# 4. Charger insights
# --------------------------------------------------

top_charger = charger.loc[charger["Sessions"].idxmax()]
highest_demand_charger = charger.loc[charger["TotalDemand"].idxmax()]


# --------------------------------------------------
# 5. User insights
# --------------------------------------------------

top_user = user.loc[user["Sessions"].idxmax()]
highest_demand_user = user.loc[user["TotalDemand"].idxmax()]


# --------------------------------------------------
# 6. Peak vs non-peak insights
# --------------------------------------------------

peak_period = peak.loc[peak["Period"] == "Peak Hour"]
non_peak_period = peak.loc[peak["Period"] == "Non-Peak Hour"]


# --------------------------------------------------
# 7. Monthly insights
# --------------------------------------------------

highest_month = monthly.loc[monthly["Sessions"].idxmax()]
highest_demand_month = monthly.loc[monthly["TotalDemand"].idxmax()]


# --------------------------------------------------
# 8. Display insights
# --------------------------------------------------

print("\n" + "=" * 60)
print("EV CHARGE INTELLIGENCE - BUSINESS INSIGHTS")
print("=" * 60)


print("\n1. HOURLY INSIGHTS")
print("-" * 40)

print(
    f"Busiest hour: {int(busiest_hour['StartHour'])}:00 "
    f"with {int(busiest_hour['Sessions'])} sessions"
)

print(
    f"Highest demand hour: {int(highest_demand_hour['StartHour'])}:00 "
    f"with {highest_demand_hour['TotalDemand']:.2f} kWh"
)


print("\n2. LOCATION INSIGHTS")
print("-" * 40)

print(
    f"Most used location: {top_location['Location']} "
    f"with {int(top_location['Sessions'])} sessions"
)

print(
    f"Highest demand location: {highest_demand_location['Location']} "
    f"with {highest_demand_location['TotalDemand']:.2f} kWh"
)


print("\n3. CHARGER INSIGHTS")
print("-" * 40)

print(
    f"Most used charger: {int(top_charger['ChargerID'])} "
    f"with {int(top_charger['Sessions'])} sessions"
)

print(
    f"Highest demand charger: {int(highest_demand_charger['ChargerID'])} "
    f"with {highest_demand_charger['TotalDemand']:.2f} kWh"
)


print("\n4. USER INSIGHTS")
print("-" * 40)

print(
    f"Most active user: {int(top_user['UserID'])} "
    f"with {int(top_user['Sessions'])} sessions"
)

print(
    f"Highest demand user: {int(highest_demand_user['UserID'])} "
    f"with {highest_demand_user['TotalDemand']:.2f} kWh"
)


print("\n5. PEAK VS NON-PEAK")
print("-" * 40)

if not peak_period.empty:
    print(
        f"Peak sessions: "
        f"{int(peak_period.iloc[0]['Sessions'])}"
    )

    print(
        f"Peak average demand: "
        f"{peak_period.iloc[0]['AverageDemand']:.2f} kWh"
    )

    print(
        f"Peak average duration: "
        f"{peak_period.iloc[0]['AverageDuration']:.2f} minutes"
    )

if not non_peak_period.empty:
    print(
        f"Non-peak sessions: "
        f"{int(non_peak_period.iloc[0]['Sessions'])}"
    )

    print(
        f"Non-peak average demand: "
        f"{non_peak_period.iloc[0]['AverageDemand']:.2f} kWh"
    )

    print(
        f"Non-peak average duration: "
        f"{non_peak_period.iloc[0]['AverageDuration']:.2f} minutes"
    )


print("\n6. MONTHLY INSIGHTS")
print("-" * 40)

print(
    f"Highest session month: "
    f"{int(highest_month['Year'])}-"
    f"{int(highest_month['Month']):02d} "
    f"with {int(highest_month['Sessions'])} sessions"
)

print(
    f"Highest demand month: "
    f"{int(highest_demand_month['Year'])}-"
    f"{int(highest_demand_month['Month']):02d} "
    f"with {highest_demand_month['TotalDemand']:.2f} kWh"
)


print("\n" + "=" * 60)
print("Analysis completed successfully.")
print("=" * 60)