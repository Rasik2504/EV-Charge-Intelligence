# EV Charge Intelligence

An end-to-end EV charging data engineering and analytics project built with Python, Pandas, Matplotlib, and Streamlit.

The project processes **72K+ EV charging sessions** through data cleaning, validation, transformation, analytics, business insights, visualization, and an interactive dashboard.

---

## Project Overview

EV charging networks generate large amounts of operational data such as charging sessions, energy demand, charger usage, locations, and user activity.

**EV Charge Intelligence** transforms raw charging transaction data into reliable analytics datasets and an interactive dashboard that can be used to understand:

* Charging demand patterns
* Peak charging hours
* Location performance
* Charger utilization
* User charging behavior
* Monthly charging trends
* Peak vs non-peak charging activity

The project is designed as a small end-to-end **data engineering pipeline**, from raw data ingestion to business-facing analytics.

---

## Project Architecture

```text
Raw EV Charging Dataset
          |
          v
    Data Cleaning
          |
          v
 Data Validation
          |
          v
 Data Transformation
          |
          v
   Analytics Tables
          |
          v
 Business Insights
          |
          v
   Visualization
          |
          v
 Interactive Dashboard
```

---

## Tech Stack

* **Python** — Core programming language
* **Pandas** — Data processing and transformation
* **Matplotlib** — Data visualization
* **Streamlit** — Interactive dashboard
* **Git & GitHub** — Version control
* **CSV** — Data storage and analytics outputs

---

## Dataset

The project uses a public EV charging transactions dataset containing charging session information.

### Original dataset

* **72,856** charging sessions
* **2,337** users
* **2,119** chargers
* **14** locations
* **2** charger companies
* **2** charger types
* **13** source columns

The raw dataset is intentionally excluded from the GitHub repository using `.gitignore`.

---

## Data Engineering Pipeline

### 1. Data Ingestion

The pipeline loads the raw EV charging dataset using Pandas.

The original data contains information such as:

* User ID
* Charger ID
* Charger company
* Location
* Charger type
* Start date/time
* End date/time
* Charging duration
* Energy demand

---

### 2. Data Cleaning

The cleaning pipeline performs:

* Duplicate detection and removal
* Timestamp parsing
* Invalid timestamp validation
* Duration validation
* Demand validation
* ID validation
* Category validation
* Location standardization
* Date and time feature extraction

Invalid charging sessions where the end timestamp occurs before the start timestamp are removed.

---

### 3. Data Validation

The pipeline validates the cleaned dataset for:

* Missing values
* Duplicate records
* Negative duration
* Negative demand
* Invalid timestamps
* Invalid IDs
* Invalid categorical values
* Session and demand consistency

Final cleaned dataset:

* **72,826 valid sessions**
* **0 missing values**
* **0 duplicate records**
* **0 negative durations**
* **0 negative demand values**

---

### 4. Data Transformation

The transformation layer generates seven analytical datasets:

```text
hourly_metrics.csv
daily_metrics.csv
location_metrics.csv
charger_metrics.csv
user_metrics.csv
peak_hour_metrics.csv
monthly_metrics.csv
```

These datasets provide different analytical views of the charging network.

---

## Analytics

The project analyzes charging activity across multiple dimensions.

### Hourly Analytics

Identifies:

* Busiest charging hours
* Hourly demand
* Average charging demand
* Average charging duration

### Location Analytics

Analyzes:

* Sessions by location
* Total energy demand
* Average demand
* Average duration
* Unique users
* Active chargers

### Charger Analytics

Analyzes:

* Charger utilization
* Total sessions
* Total demand
* Average demand
* Average duration
* Unique users
* Charger location and type

### User Analytics

Analyzes:

* Sessions per user
* Total energy consumption
* Average demand
* Average duration
* Unique chargers used
* Unique locations visited

### Peak vs Non-Peak Analytics

Compares:

* Number of sessions
* Average demand
* Average duration
* Unique users
* Active chargers

### Monthly Analytics

Tracks:

* Monthly sessions
* Monthly energy demand
* Average demand
* Average duration
* Active users
* Active chargers

---

## Key Business Insights

The analysis identified several important patterns:

* **18:00** was the busiest charging hour with **6,506 sessions**.
* **Apartment** locations recorded the highest total demand with **263,103.12 kWh**.
* Peak hours recorded **27,104 sessions**.
* Peak-hour charging had an average demand of **19.59 kWh per session**.
* Non-peak charging had an average demand of **16.17 kWh per session**.
* **August 2022** recorded the highest activity with **8,083 sessions**.
* August 2022 also recorded the highest monthly demand with **143,041.27 kWh**.
* **UserID 0** was identified as a significant usage outlier with **31,553 sessions**, requiring further investigation.

---

## Data Visualizations

The project generates visualizations for:

* EV charging sessions by hour
* Charging demand by location
* Monthly charging demand trends
* Peak vs non-peak average demand

Generated charts are stored under:

```text
data/analytics/charts/
```

Generated analytics data and charts are excluded from GitHub because they are pipeline outputs.

---

## Interactive Dashboard

The project includes a Streamlit dashboard for exploring the processed analytics.

The dashboard provides:

### Key Performance Indicators

* Total charging sessions
* Total energy demand
* Number of users
* Number of chargers
* Number of locations

### Dashboard Analysis

* Charging activity by hour
* Hourly energy demand
* Location-wise demand
* Location performance table
* Monthly charging trends
* Peak vs non-peak comparison
* Top chargers
* Top users
* Business insights

### Run the dashboard

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Start the dashboard:

```bash
streamlit run app.py
```

The dashboard will open in your browser.

---

## Running the Complete Pipeline

The project includes a pipeline orchestrator that runs the complete workflow.

Run:

```bash
python src/pipeline.py
```

This executes:

```text
clean.py
   |
   v
transform.py
   |
   v
analyze.py
   |
   v
visualize.py
```

This provides a single command for rebuilding the processed data, analytics, insights, and visualizations.

---

## Project Structure

```text
EV-ChargeIntelligence/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── clean.py
│   ├── transform.py
│   ├── analyze.py
│   ├── visualize.py
│   └── pipeline.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── analytics/
│
└── venv/
```

### Source Code

**`clean.py`**

Cleans and validates the raw charging data.

**`transform.py`**

Creates analytical datasets from the cleaned data.

**`analyze.py`**

Extracts business insights from the analytical datasets.

**`visualize.py`**

Generates charts using Matplotlib.

**`pipeline.py`**

Orchestrates the complete data processing workflow.

**`app.py`**

Provides the interactive Streamlit dashboard.

---

## Data Quality

The final processing pipeline produced:

| Metric                    |          Result |
| ------------------------- | --------------: |
| Valid charging sessions   |          72,826 |
| Total demand              | 1,270,112.1 kWh |
| Missing values            |               0 |
| Duplicate records         |               0 |
| Negative duration records |               0 |
| Negative demand records   |               0 |
| Users                     |           2,337 |
| Valid chargers            |           2,118 |
| Locations                 |              14 |
| Analytics tables          |               7 |

Session and demand totals were validated across the generated analytical datasets.

---

## Data Privacy & Repository Design

The raw dataset and generated analytics files are excluded from version control.

The `.gitignore` file excludes:

```text
venv/
__pycache__/
*.pyc
.env
data/raw/*.csv
data/processed/
data/analytics/
```

This keeps the repository focused on the reproducible pipeline and source code rather than generated data files.

---

## Skills Demonstrated

This project demonstrates practical experience with:

* Python programming
* Pandas
* Data cleaning
* Data validation
* Data transformation
* Exploratory data analysis
* Business analytics
* Data aggregation
* Data quality checks
* Data visualization
* Streamlit dashboards
* Pipeline orchestration
* Git
* GitHub
* Project documentation

---

## Future Improvements

Possible future enhancements include:

* Automated data ingestion from an external source
* SQL-based analytical storage
* Cloud data warehouse integration
* Scheduled pipeline execution
* Automated data quality testing
* Interactive dashboard filters
* Charger utilization forecasting
* EV charging demand prediction
* Anomaly detection
* Docker containerization
* Cloud deployment

---

## Project Status

**Completed**

The current version includes:

* End-to-end data processing pipeline
* Data cleaning and validation
* Analytics transformation layer
* Business insights
* Data visualizations
* Interactive Streamlit dashboard
* Pipeline orchestration
* Git/GitHub version control
* Project documentation

---

## Author

**Rasik Rahman**

B.Tech — Artificial Intelligence & Data Science

GitHub: [Rasik2504](https://github.com/Rasik2504)
