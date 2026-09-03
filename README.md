# EV-ChargeIntelligence

## EV Charging Data Engineering & Station Intelligence Platform

An end-to-end Data Engineering project for processing and analyzing EV charging session data.

## Project Status

🚧 Currently under development.

## Planned Technologies

- Python
- Pandas
- PostgreSQL
- SQL
- Apache Airflow
- Power BI
- Git/GitHub

## Project Progress

### Day 1 - Data Ingestion & Profiling
- Loaded raw EV charging dataset
- Performed dataset profiling
- Checked missing values
- Checked duplicate records
- Validated IDs and categorical fields
- Investigated timestamp and duration anomalies

### Day 2 - Data Cleaning & Transformation
- Removed exact duplicate records
- Removed invalid timestamp-order records
- Validated charging duration
- Validated energy demand
- Standardized location values
- Created timestamp-based features
- Created peak-hour indicator
- Generated cleaned dataset
- Added automated validation checks

Final cleaned dataset:
- 72,826 charging sessions
- 15 analytical columns
- 0 missing values
- 0 duplicate records
- 0 negative demand values
- 0 negative duration values

### Day 3 - Data Transformation & Analytics

- Created analytics transformation pipeline
- Generated hourly charging metrics
- Generated daily charging metrics
- Generated location-level metrics
- Generated charger-level metrics
- Generated user-level metrics
- Generated peak vs non-peak metrics
- Generated monthly charging metrics
- Added analytics validation checks
- Validated session and demand totals across analytics tables

Final analytics datasets:

- 7 analytics tables generated
- 72,826 charging sessions preserved
- 1,270,112.1 kWh total demand preserved
- 0 missing values
- 0 duplicate records
- 2,118 valid chargers
- 2,337 users
- 14 locations
- Analytics CSV files added to `.gitignore`