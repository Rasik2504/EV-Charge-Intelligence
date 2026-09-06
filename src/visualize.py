import pandas as pd
import matplotlib.pyplot as plt
import os


# --------------------------------------------------
# 1. Load analytics datasets
# --------------------------------------------------

base_path = "data/analytics"

hourly = pd.read_csv(os.path.join(base_path, "hourly_metrics.csv"))
location = pd.read_csv(os.path.join(base_path, "location_metrics.csv"))
monthly = pd.read_csv(os.path.join(base_path, "monthly_metrics.csv"))
peak = pd.read_csv(os.path.join(base_path, "peak_hour_metrics.csv"))


# --------------------------------------------------
# 2. Create output directory
# --------------------------------------------------

output_path = "data/analytics/charts"
os.makedirs(output_path, exist_ok=True)


# --------------------------------------------------
# 3. Hourly sessions chart
# --------------------------------------------------

plt.figure(figsize=(10, 5))

plt.bar(
    hourly["StartHour"],
    hourly["Sessions"]
)

plt.xlabel("Hour of Day")
plt.ylabel("Number of Sessions")
plt.title("EV Charging Sessions by Hour")
plt.xticks(range(0, 24))

plt.tight_layout()

plt.savefig(
    os.path.join(output_path, "hourly_sessions.png")
)

plt.close()


# --------------------------------------------------
# 4. Location demand chart
# --------------------------------------------------

location_sorted = location.sort_values(
    "TotalDemand",
    ascending=False
)

plt.figure(figsize=(10, 6))

plt.barh(
    location_sorted["Location"],
    location_sorted["TotalDemand"]
)

plt.xlabel("Total Demand (kWh)")
plt.ylabel("Location")
plt.title("EV Charging Demand by Location")

plt.gca().invert_yaxis()

plt.tight_layout()

plt.savefig(
    os.path.join(output_path, "location_demand.png")
)

plt.close()


# --------------------------------------------------
# 5. Monthly demand chart
# --------------------------------------------------

monthly["MonthLabel"] = (
    monthly["Year"].astype(str)
    + "-"
    + monthly["Month"].astype(str).str.zfill(2)
)

plt.figure(figsize=(10, 5))

plt.plot(
    monthly["MonthLabel"],
    monthly["TotalDemand"],
    marker="o"
)

plt.xlabel("Month")
plt.ylabel("Total Demand (kWh)")
plt.title("Monthly EV Charging Demand")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    os.path.join(output_path, "monthly_demand.png")
)

plt.close()


# --------------------------------------------------
# 6. Peak vs non-peak demand chart
# --------------------------------------------------

plt.figure(figsize=(7, 5))

plt.bar(
    peak["Period"],
    peak["AverageDemand"]
)

plt.xlabel("Charging Period")
plt.ylabel("Average Demand (kWh)")
plt.title("Peak vs Non-Peak Average Demand")

plt.tight_layout()

plt.savefig(
    os.path.join(output_path, "peak_vs_nonpeak.png")
)

plt.close()


# --------------------------------------------------
# 7. Display completion message
# --------------------------------------------------

print("\n" + "=" * 60)
print("EV CHARGE INTELLIGENCE - VISUALIZATION")
print("=" * 60)

print("\nCharts generated successfully:")

print("- hourly_sessions.png")
print("- location_demand.png")
print("- monthly_demand.png")
print("- peak_vs_nonpeak.png")

print("\nOutput directory:")
print(output_path)

print("\nVisualization completed successfully.")

print("=" * 60)