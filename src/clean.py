import pandas as pd
from pathlib import Path


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw" / "ev_charging.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_FILE = PROCESSED_DIR / "ev_charging_cleaned.csv"


# ============================================================
# 2. LOAD RAW DATA
# ============================================================

print("=" * 60)
print("EV CHARGE INTELLIGENCE - DATA CLEANING")
print("=" * 60)

print("\nLoading raw dataset...")

df = pd.read_csv(RAW_FILE)

print(f"Raw dataset shape: {df.shape}")


# ============================================================
# 3. REMOVE EXACT DUPLICATES
# ============================================================

print("\n" + "-" * 60)
print("STEP 1: DUPLICATE CHECK")
print("-" * 60)

duplicate_count = df.duplicated().sum()

print(f"Exact duplicate rows found: {duplicate_count}")

if duplicate_count > 0:
    df = df.drop_duplicates().copy()

print(f"Shape after duplicate removal: {df.shape}")


# ============================================================
# 4. CREATE ACCURATE TIMESTAMPS
# ============================================================

print("\n" + "-" * 60)
print("STEP 2: TIMESTAMP CREATION")
print("-" * 60)

df["StartTimestamp"] = pd.to_datetime(
    df["StartDay"].astype(str) + " " + df["StartTime"].astype(str),
    errors="coerce"
)

df["EndTimestamp"] = pd.to_datetime(
    df["EndDay"].astype(str) + " " + df["EndTime"].astype(str),
    errors="coerce"
)

invalid_start = df["StartTimestamp"].isna().sum()
invalid_end = df["EndTimestamp"].isna().sum()

print(f"Invalid start timestamps: {invalid_start}")
print(f"Invalid end timestamps: {invalid_end}")


# ============================================================
# 5. CALCULATE DURATION FROM TIMESTAMPS
# ============================================================

print("\n" + "-" * 60)
print("STEP 3: DURATION VALIDATION")
print("-" * 60)

df["CalculatedDuration"] = (
    df["EndTimestamp"] - df["StartTimestamp"]
).dt.total_seconds() / 60

df["CalculatedDuration"] = df["CalculatedDuration"].round().astype("Int64")

negative_calculated = (
    df["CalculatedDuration"].notna()
    & (df["CalculatedDuration"] < 0)
)

print(
    "Rows where EndTimestamp is before StartTimestamp:",
    negative_calculated.sum()
)


# ============================================================
# 6. REMOVE IMPOSSIBLE TIMESTAMP RECORDS
# ============================================================

print("\nRemoving records with invalid timestamp ordering...")

invalid_order = (
    df["StartTimestamp"].notna()
    & df["EndTimestamp"].notna()
    & (df["StartTimestamp"] > df["EndTimestamp"])
)

removed_invalid_order = invalid_order.sum()

df = df[~invalid_order].copy()

print(f"Removed rows: {removed_invalid_order}")


# ============================================================
# 7. HANDLE SOURCE DURATION
# ============================================================

print("\n" + "-" * 60)
print("STEP 4: SOURCE DURATION CHECK")
print("-" * 60)

df["DurationDifference"] = (
    df["Duration"] - df["CalculatedDuration"].astype(float)
)

large_difference = (
    df["DurationDifference"].abs() > 1
).sum()

print(
    "Rows with duration difference greater than 1 minute:",
    large_difference
)

print(
    "\nNote: Source Duration is stored as whole minutes while "
    "timestamps contain seconds."
)

print(
    "Therefore, timestamp rounding differences are retained "
    "rather than unnecessarily deleting valid records."
)


# ============================================================
# 8. FIX NEGATIVE SOURCE DURATIONS
# ============================================================

negative_duration = (df["Duration"] < 0).sum()

print(f"\nNegative Duration values before correction: {negative_duration}")

if negative_duration > 0:
    valid_calculated_duration = (
        df["CalculatedDuration"].notna()
        & (df["CalculatedDuration"] >= 0)
    )

    correction_mask = (
        (df["Duration"] < 0)
        & valid_calculated_duration
    )

    df.loc[correction_mask, "Duration"] = (
        df.loc[correction_mask, "CalculatedDuration"]
    )

print(
    "Negative Duration values after correction:",
    (df["Duration"] < 0).sum()
)


# ============================================================
# 9. DEMAND VALIDATION
# ============================================================

print("\n" + "-" * 60)
print("STEP 5: DEMAND VALIDATION")
print("-" * 60)

negative_demand = (df["Demand"] < 0).sum()

print(f"Negative demand records: {negative_demand}")

if negative_demand > 0:
    df = df[df["Demand"] >= 0].copy()

print(f"Rows after demand validation: {len(df)}")


# ============================================================
# 10. ID VALIDATION
# ============================================================

print("\n" + "-" * 60)
print("STEP 6: ID VALIDATION")
print("-" * 60)

invalid_users = (
    df["UserID"].isna()
    | (df["UserID"] < 0)
).sum()

invalid_chargers = (
    df["ChargerID"].isna()
    | (df["ChargerID"] <= 0)
).sum()

print(f"Invalid UserID records: {invalid_users}")
print(f"Invalid ChargerID records: {invalid_chargers}")


# ============================================================
# 11. CATEGORY VALIDATION
# ============================================================

print("\n" + "-" * 60)
print("STEP 7: CATEGORY VALIDATION")
print("-" * 60)

valid_company_values = {0, 1}
valid_charger_type_values = {0, 1}

invalid_company = (
    ~df["ChargerCompany"].isin(valid_company_values)
).sum()

invalid_charger_type = (
    ~df["ChargerType"].isin(valid_charger_type_values)
).sum()

print(f"Invalid ChargerCompany values: {invalid_company}")
print(f"Invalid ChargerType values: {invalid_charger_type}")


# ============================================================
# 12. STANDARDIZE LOCATION
# ============================================================

print("\n" + "-" * 60)
print("STEP 8: LOCATION STANDARDIZATION")
print("-" * 60)

df["Location"] = (
    df["Location"]
    .astype("string")
    .str.strip()
    .str.lower()
)

print("Location values standardized.")


# ============================================================
# 13. CREATE TIME FEATURES
# ============================================================

print("\n" + "-" * 60)
print("STEP 9: TIME FEATURE ENGINEERING")
print("-" * 60)

df["StartDate"] = df["StartTimestamp"].dt.date

df["StartHour"] = df["StartTimestamp"].dt.hour

df["StartDayOfWeek"] = df["StartTimestamp"].dt.day_name()

df["StartMonth"] = df["StartTimestamp"].dt.month

df["StartYear"] = df["StartTimestamp"].dt.year


# ============================================================
# 14. CREATE PEAK-HOUR FEATURE
# ============================================================

# Peak charging period:
# 5 PM - 9 PM

df["IsPeakHour"] = df["StartHour"].between(17, 21)

print("Created time features:")
print("- StartDate")
print("- StartHour")
print("- StartDayOfWeek")
print("- StartMonth")
print("- StartYear")
print("- IsPeakHour")


# ============================================================
# 15. DROP TEMPORARY / REDUNDANT COLUMNS
# ============================================================

columns_to_drop = [
    "StartDay",
    "StartTime",
    "EndDay",
    "EndTime",
    "StartDatetime",
    "EndDatetime",
    "CalculatedDuration",
    "DurationDifference"
]

df = df.drop(
    columns=columns_to_drop,
    errors="ignore"
)


# ============================================================
# 16. REORDER FINAL COLUMNS
# ============================================================

final_columns = [
    "UserID",
    "ChargerID",
    "ChargerCompany",
    "Location",
    "ChargerType",
    "StartTimestamp",
    "EndTimestamp",
    "Duration",
    "Demand",
    "StartDate",
    "StartHour",
    "StartDayOfWeek",
    "StartMonth",
    "StartYear",
    "IsPeakHour"
]

df = df[final_columns]


# ============================================================
# 17. CREATE PROCESSED DIRECTORY
# ============================================================

PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 18. SAVE CLEAN DATASET
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# 19. FINAL VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("FINAL VALIDATION")
print("=" * 60)

print(f"\nFinal dataset shape: {df.shape}")

print("\nFinal columns:")
for column in df.columns:
    print(f"- {column}")

print("\nMissing values:")
print(df.isna().sum())

print("\nExact duplicate rows:", df.duplicated().sum())

print(
    "\nNegative Duration values:",
    (df["Duration"] < 0).sum()
)

print(
    "Negative Demand values:",
    (df["Demand"] < 0).sum()
)

print(
    "Invalid timestamp ordering:",
    (df["StartTimestamp"] > df["EndTimestamp"]).sum()
)

print(
    "Zero-duration records:",
    (df["Duration"] == 0).sum()
)

print("\nLocation distribution:")
print(df["Location"].value_counts())

print("\nPeak-hour distribution:")
print(df["IsPeakHour"].value_counts())

print("\nProcessed file:")
print(OUTPUT_FILE)

print("\n" + "=" * 60)
print("CLEANING COMPLETED")
print("=" * 60)