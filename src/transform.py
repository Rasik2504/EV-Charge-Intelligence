import pandas as pd
from pathlib import Path


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "ev_charging_cleaned.csv"
)

ANALYTICS_DIR = BASE_DIR / "data" / "analytics"


# ============================================================
# 2. LOAD CLEANED DATA
# ============================================================

print("=" * 60)
print("EV CHARGE INTELLIGENCE - DATA TRANSFORMATION")
print("=" * 60)

print("\nLoading cleaned dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Input dataset shape: {df.shape}")


# ============================================================
# 3. PREPARE DATETIME COLUMNS
# ============================================================

print("\n" + "-" * 60)
print("STEP 1: PREPARING DATETIME DATA")
print("-" * 60)

df["StartTimestamp"] = pd.to_datetime(
    df["StartTimestamp"],
    errors="coerce"
)

df["EndTimestamp"] = pd.to_datetime(
    df["EndTimestamp"],
    errors="coerce"
)

df["StartDate"] = pd.to_datetime(
    df["StartDate"],
    errors="coerce"
)

print("Datetime columns prepared.")


# ============================================================
# 4. CREATE ANALYTICS DIRECTORY
# ============================================================

ANALYTICS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

print(f"\nAnalytics output directory: {ANALYTICS_DIR}")


# ============================================================
# 5. HOURLY METRICS
# ============================================================

print("\n" + "-" * 60)
print("STEP 2: HOURLY METRICS")
print("-" * 60)

hourly_metrics = (
    df.groupby("StartHour")
    .agg(
        Sessions=("UserID", "count"),
        TotalDemand=("Demand", "sum"),
        AverageDemand=("Demand", "mean"),
        AverageDuration=("Duration", "mean")
    )
    .reset_index()
)

hourly_metrics["TotalDemand"] = hourly_metrics["TotalDemand"].round(2)
hourly_metrics["AverageDemand"] = hourly_metrics["AverageDemand"].round(2)
hourly_metrics["AverageDuration"] = hourly_metrics["AverageDuration"].round(2)

hourly_metrics.to_csv(
    ANALYTICS_DIR / "hourly_metrics.csv",
    index=False
)

print(f"Hourly rows created: {len(hourly_metrics)}")


# ============================================================
# 6. DAILY METRICS
# ============================================================

print("\n" + "-" * 60)
print("STEP 3: DAILY METRICS")
print("-" * 60)

daily_metrics = (
    df.groupby("StartDate")
    .agg(
        Sessions=("UserID", "count"),
        TotalDemand=("Demand", "sum"),
        AverageDemand=("Demand", "mean"),
        AverageDuration=("Duration", "mean"),
        UniqueUsers=("UserID", "nunique"),
        ActiveChargers=("ChargerID", "nunique")
    )
    .reset_index()
)

daily_metrics["TotalDemand"] = daily_metrics["TotalDemand"].round(2)
daily_metrics["AverageDemand"] = daily_metrics["AverageDemand"].round(2)
daily_metrics["AverageDuration"] = daily_metrics["AverageDuration"].round(2)

daily_metrics.to_csv(
    ANALYTICS_DIR / "daily_metrics.csv",
    index=False
)

print(f"Daily rows created: {len(daily_metrics)}")


# ============================================================
# 7. LOCATION METRICS
# ============================================================

print("\n" + "-" * 60)
print("STEP 4: LOCATION METRICS")
print("-" * 60)

location_metrics = (
    df.groupby("Location")
    .agg(
        Sessions=("UserID", "count"),
        TotalDemand=("Demand", "sum"),
        AverageDemand=("Demand", "mean"),
        AverageDuration=("Duration", "mean"),
        UniqueUsers=("UserID", "nunique"),
        ActiveChargers=("ChargerID", "nunique")
    )
    .reset_index()
)

location_metrics["TotalDemand"] = location_metrics["TotalDemand"].round(2)
location_metrics["AverageDemand"] = location_metrics["AverageDemand"].round(2)
location_metrics["AverageDuration"] = location_metrics["AverageDuration"].round(2)

location_metrics = location_metrics.sort_values(
    "TotalDemand",
    ascending=False
)

location_metrics.to_csv(
    ANALYTICS_DIR / "location_metrics.csv",
    index=False
)

print(f"Location rows created: {len(location_metrics)}")


# ============================================================
# 8. CHARGER METRICS
# ============================================================

print("\n" + "-" * 60)
print("STEP 5: CHARGER METRICS")
print("-" * 60)

charger_metrics = (
    df.groupby("ChargerID")
    .agg(
        Sessions=("UserID", "count"),
        TotalDemand=("Demand", "sum"),
        AverageDemand=("Demand", "mean"),
        AverageDuration=("Duration", "mean"),
        UniqueUsers=("UserID", "nunique"),
        Location=("Location", "first"),
        ChargerCompany=("ChargerCompany", "first"),
        ChargerType=("ChargerType", "first")
    )
    .reset_index()
)

charger_metrics["TotalDemand"] = charger_metrics["TotalDemand"].round(2)
charger_metrics["AverageDemand"] = charger_metrics["AverageDemand"].round(2)
charger_metrics["AverageDuration"] = charger_metrics["AverageDuration"].round(2)

charger_metrics = charger_metrics.sort_values(
    "Sessions",
    ascending=False
)

charger_metrics.to_csv(
    ANALYTICS_DIR / "charger_metrics.csv",
    index=False
)

print(f"Charger rows created: {len(charger_metrics)}")


# ============================================================
# 9. USER METRICS
# ============================================================

print("\n" + "-" * 60)
print("STEP 6: USER METRICS")
print("-" * 60)

user_metrics = (
    df.groupby("UserID")
    .agg(
        Sessions=("ChargerID", "count"),
        TotalDemand=("Demand", "sum"),
        AverageDemand=("Demand", "mean"),
        AverageDuration=("Duration", "mean"),
        UniqueChargers=("ChargerID", "nunique"),
        UniqueLocations=("Location", "nunique")
    )
    .reset_index()
)

user_metrics["TotalDemand"] = user_metrics["TotalDemand"].round(2)
user_metrics["AverageDemand"] = user_metrics["AverageDemand"].round(2)
user_metrics["AverageDuration"] = user_metrics["AverageDuration"].round(2)

user_metrics = user_metrics.sort_values(
    "Sessions",
    ascending=False
)

user_metrics.to_csv(
    ANALYTICS_DIR / "user_metrics.csv",
    index=False
)

print(f"User rows created: {len(user_metrics)}")


# ============================================================
# 10. PEAK-HOUR METRICS
# ============================================================

print("\n" + "-" * 60)
print("STEP 7: PEAK-HOUR METRICS")
print("-" * 60)

peak_hour_metrics = (
    df.groupby("IsPeakHour")
    .agg(
        Sessions=("UserID", "count"),
        TotalDemand=("Demand", "sum"),
        AverageDemand=("Demand", "mean"),
        AverageDuration=("Duration", "mean"),
        UniqueUsers=("UserID", "nunique"),
        ActiveChargers=("ChargerID", "nunique")
    )
    .reset_index()
)

peak_hour_metrics["Period"] = peak_hour_metrics[
    "IsPeakHour"
].map(
    {
        True: "Peak Hour",
        False: "Non-Peak Hour"
    }
)

peak_hour_metrics["TotalDemand"] = peak_hour_metrics["TotalDemand"].round(2)
peak_hour_metrics["AverageDemand"] = peak_hour_metrics["AverageDemand"].round(2)
peak_hour_metrics["AverageDuration"] = peak_hour_metrics["AverageDuration"].round(2)

peak_hour_metrics = peak_hour_metrics[
    [
        "Period",
        "IsPeakHour",
        "Sessions",
        "TotalDemand",
        "AverageDemand",
        "AverageDuration",
        "UniqueUsers",
        "ActiveChargers"
    ]
]

peak_hour_metrics.to_csv(
    ANALYTICS_DIR / "peak_hour_metrics.csv",
    index=False
)

print(f"Peak-hour rows created: {len(peak_hour_metrics)}")


# ============================================================
# 11. MONTHLY METRICS
# ============================================================

print("\n" + "-" * 60)
print("STEP 8: MONTHLY METRICS")
print("-" * 60)

df["Year"] = df["StartTimestamp"].dt.year
df["Month"] = df["StartTimestamp"].dt.month

monthly_metrics = (
    df.groupby(["Year", "Month"])
    .agg(
        Sessions=("UserID", "count"),
        TotalDemand=("Demand", "sum"),
        AverageDemand=("Demand", "mean"),
        AverageDuration=("Duration", "mean"),
        UniqueUsers=("UserID", "nunique"),
        ActiveChargers=("ChargerID", "nunique")
    )
    .reset_index()
)

monthly_metrics["TotalDemand"] = monthly_metrics["TotalDemand"].round(2)
monthly_metrics["AverageDemand"] = monthly_metrics["AverageDemand"].round(2)
monthly_metrics["AverageDuration"] = monthly_metrics["AverageDuration"].round(2)

monthly_metrics.to_csv(
    ANALYTICS_DIR / "monthly_metrics.csv",
    index=False
)

print(f"Monthly rows created: {len(monthly_metrics)}")


# ============================================================
# 12. TRANSFORMATION VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("TRANSFORMATION VALIDATION")
print("=" * 60)

print("\nGenerated analytics tables:")

analytics_files = [
    "hourly_metrics.csv",
    "daily_metrics.csv",
    "location_metrics.csv",
    "charger_metrics.csv",
    "user_metrics.csv",
    "peak_hour_metrics.csv",
    "monthly_metrics.csv"
]

for file_name in analytics_files:
    file_path = ANALYTICS_DIR / file_name

    check_df = pd.read_csv(file_path)

    print(
        f"- {file_name:<25} "
        f"{check_df.shape[0]:>6} rows × "
        f"{check_df.shape[1]:>2} columns"
    )


# ============================================================
# 13. DISPLAY IMPORTANT RESULTS
# ============================================================

print("\n" + "-" * 60)
print("TOP LOCATIONS BY TOTAL DEMAND")
print("-" * 60)

print(
    location_metrics[
        [
            "Location",
            "Sessions",
            "TotalDemand",
            "AverageDemand"
        ]
    ].head(5).to_string(index=False)
)


print("\n" + "-" * 60)
print("TOP 5 CHARGERS BY NUMBER OF SESSIONS")
print("-" * 60)

print(
    charger_metrics[
        [
            "ChargerID",
            "Sessions",
            "TotalDemand",
            "AverageDemand"
        ]
    ].head(5).to_string(index=False)
)


print("\n" + "-" * 60)
print("PEAK VS NON-PEAK")
print("-" * 60)

print(
    peak_hour_metrics.to_string(index=False)
)


print("\n" + "=" * 60)
print("TRANSFORMATION COMPLETED")
print("=" * 60)

print(f"\nAnalytics files saved to:")
print(ANALYTICS_DIR)