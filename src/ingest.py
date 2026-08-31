import pandas as pd


# ============================================================
# EV CHARGE INTELLIGENCE
# DATA INGESTION + DATA PROFILING + DATA QUALITY ANALYSIS
# ============================================================


# ============================================================
# 1. LOAD RAW DATA
# ============================================================

file_path = "data/raw/ev_charging.csv"

df = pd.read_csv(file_path)

print("Data loaded successfully!")


# ============================================================
# 2. BASIC DATA OVERVIEW
# ============================================================

print("\n" + "=" * 60)
print("FIRST 5 ROWS")
print("=" * 60)

print(df.head())


print("\n" + "=" * 60)
print("DATASET SHAPE")
print("=" * 60)

print(df.shape)


print("\n" + "=" * 60)
print("COLUMN NAMES")
print("=" * 60)

print(df.columns.tolist())


# ============================================================
# 3. DATASET INFORMATION
# ============================================================

print("\n" + "=" * 60)
print("DATASET INFORMATION")
print("=" * 60)

df.info()


# ============================================================
# 4. MISSING VALUE CHECK
# ============================================================

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

missing_values = df.isnull().sum()

print(missing_values)

print("\nTotal missing values:", missing_values.sum())


# ============================================================
# 5. DUPLICATE CHECK
# ============================================================

print("\n" + "=" * 60)
print("DUPLICATE CHECK")
print("=" * 60)

duplicate_count = df.duplicated().sum()

print("Number of duplicate rows:", duplicate_count)


# ============================================================
# 6. BASIC STATISTICS
# ============================================================

print("\n" + "=" * 60)
print("BASIC STATISTICS")
print("=" * 60)

print(df.describe())


# ============================================================
# 7. UNIQUE VALUES
# ============================================================

print("\n" + "=" * 60)
print("UNIQUE VALUES")
print("=" * 60)

print("Unique Users:", df["UserID"].nunique())
print("Unique Chargers:", df["ChargerID"].nunique())
print("Unique Companies:", df["ChargerCompany"].nunique())
print("Unique Locations:", df["Location"].nunique())
print("Unique Charger Types:", df["ChargerType"].nunique())


# ============================================================
# 8. LOCATION DISTRIBUTION
# ============================================================

print("\n" + "=" * 60)
print("LOCATION DISTRIBUTION")
print("=" * 60)

print(df["Location"].value_counts())


# ============================================================
# 9. CHARGER TYPE DISTRIBUTION
# ============================================================

print("\n" + "=" * 60)
print("CHARGER TYPE DISTRIBUTION")
print("=" * 60)

print(df["ChargerType"].value_counts())


# ============================================================
# 10. DEMAND STATISTICS
# ============================================================

print("\n" + "=" * 60)
print("DEMAND STATISTICS")
print("=" * 60)

print(df["Demand"].describe())


# ============================================================
# 11. DURATION STATISTICS
# ============================================================

print("\n" + "=" * 60)
print("DURATION STATISTICS")
print("=" * 60)

print(df["Duration"].describe())


# ============================================================
# 12. NEGATIVE DURATION CHECK
# ============================================================

print("\n" + "=" * 60)
print("NEGATIVE DURATION CHECK")
print("=" * 60)

negative_duration = df[df["Duration"] < 0]

print("Number of negative duration records:")
print(len(negative_duration))

if len(negative_duration) > 0:
    print("\nNegative duration records:")
    print(negative_duration)


# ============================================================
# 13. CREATE ACCURATE TIMESTAMPS
# ============================================================

print("\n" + "=" * 60)
print("CREATING ACCURATE TIMESTAMPS")
print("=" * 60)

df["StartTimestamp"] = pd.to_datetime(
    df["StartDay"] + " " + df["StartTime"],
    errors="coerce"
)

df["EndTimestamp"] = pd.to_datetime(
    df["EndDay"] + " " + df["EndTime"],
    errors="coerce"
)

print("StartTimestamp and EndTimestamp created successfully.")


# ============================================================
# 14. INVALID DATETIME CHECK
# ============================================================

print("\n" + "=" * 60)
print("INVALID DATETIME CHECK")
print("=" * 60)

invalid_start_datetime = df["StartTimestamp"].isnull().sum()
invalid_end_datetime = df["EndTimestamp"].isnull().sum()

print("Invalid StartTimestamp values:", invalid_start_datetime)
print("Invalid EndTimestamp values:", invalid_end_datetime)


# ============================================================
# 15. CALCULATE ACTUAL DURATION
# ============================================================

df["CalculatedDuration"] = (
    df["EndTimestamp"] - df["StartTimestamp"]
).dt.total_seconds() / 60


print("\n" + "=" * 60)
print("DURATION COMPARISON")
print("=" * 60)

print(
    df[
        [
            "StartTimestamp",
            "EndTimestamp",
            "Duration",
            "CalculatedDuration"
        ]
    ].head(10)
)


# ============================================================
# 16. DURATION MISMATCH CHECK
# ============================================================

df["DurationDifference"] = (
    df["Duration"] - df["CalculatedDuration"]
)

duration_mismatch = df[
    df["DurationDifference"].abs() > 1
]

print("\n" + "=" * 60)
print("DURATION MISMATCH CHECK")
print("=" * 60)

print(
    "Number of records with duration mismatch:",
    len(duration_mismatch)
)


# ============================================================
# 17. INVALID TIMESTAMP ORDER
# ============================================================

invalid_timestamp = df[
    df["StartTimestamp"] >= df["EndTimestamp"]
]

print("\n" + "=" * 60)
print("INVALID TIMESTAMP ORDER CHECK")
print("=" * 60)

print(
    "Records where StartTimestamp >= EndTimestamp:",
    len(invalid_timestamp)
)


# ============================================================
# 18. NEGATIVE CALCULATED DURATION
# ============================================================

negative_calculated_duration = df[
    df["CalculatedDuration"] < 0
]

print("\n" + "=" * 60)
print("NEGATIVE CALCULATED DURATION")
print("=" * 60)

print(
    "Records with negative calculated duration:",
    len(negative_calculated_duration)
)


# ============================================================
# 19. NEGATIVE DEMAND CHECK
# ============================================================

negative_demand = df[
    df["Demand"] < 0
]

print("\n" + "=" * 60)
print("NEGATIVE DEMAND CHECK")
print("=" * 60)

print(
    "Records with negative demand:",
    len(negative_demand)
)


# ============================================================
# 20. ZERO DURATION CHECK
# ============================================================

zero_duration = df[
    df["Duration"] == 0
]

print("\n" + "=" * 60)
print("ZERO DURATION CHECK")
print("=" * 60)

print(
    "Records with zero duration:",
    len(zero_duration)
)


# ============================================================
# 21. INVALID USER ID CHECK
# ============================================================

invalid_user_id = df[
    df["UserID"] < 0
]

print("\n" + "=" * 60)
print("USER ID VALIDATION")
print("=" * 60)

print(
    "Records with invalid UserID:",
    len(invalid_user_id)
)


# ============================================================
# 22. INVALID CHARGER ID CHECK
# ============================================================

invalid_charger_id = df[
    df["ChargerID"] <= 0
]

print("\n" + "=" * 60)
print("CHARGER ID VALIDATION")
print("=" * 60)

print(
    "Records with invalid ChargerID:",
    len(invalid_charger_id)
)


# ============================================================
# 23. INVALID CHARGER COMPANY CHECK
# ============================================================

valid_companies = [0, 1]

invalid_company = df[
    ~df["ChargerCompany"].isin(valid_companies)
]

print("\n" + "=" * 60)
print("CHARGER COMPANY VALIDATION")
print("=" * 60)

print(
    "Records with invalid ChargerCompany:",
    len(invalid_company)
)


# ============================================================
# 24. INVALID CHARGER TYPE CHECK
# ============================================================

valid_charger_types = [0, 1]

invalid_charger_type = df[
    ~df["ChargerType"].isin(valid_charger_types)
]

print("\n" + "=" * 60)
print("CHARGER TYPE VALIDATION")
print("=" * 60)

print(
    "Records with invalid ChargerType:",
    len(invalid_charger_type)
)


# ============================================================
# 25. FINAL DATA QUALITY SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("FINAL DATA QUALITY SUMMARY")
print("=" * 60)

print("Original records:", len(df))
print("Original columns:", 13)

print("\nMissing values:", missing_values.sum())
print("Duplicate rows:", duplicate_count)
print("Negative durations:", len(negative_duration))
print("Negative calculated durations:", len(negative_calculated_duration))
print("Duration mismatches:", len(duration_mismatch))
print("Invalid timestamps:", len(invalid_timestamp))
print("Invalid datetime values:",
      invalid_start_datetime + invalid_end_datetime)
print("Negative demand:", len(negative_demand))
print("Zero duration:", len(zero_duration))
print("Invalid UserID:", len(invalid_user_id))
print("Invalid ChargerID:", len(invalid_charger_id))
print("Invalid ChargerCompany:", len(invalid_company))
print("Invalid ChargerType:", len(invalid_charger_type))


# ============================================================
# 26. PROFILING COMPLETE
# ============================================================

print("\n" + "=" * 60)
print("DATA PROFILING COMPLETED")
print("=" * 60)