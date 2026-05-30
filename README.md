---

# 📊 Retail Market Intelligence ETL Pipeline

## Overview

This project is an end-to-end **data engineering ETL pipeline** that ingests retail datasets from Kaggle, validates and cleans them, performs feature engineering, and loads structured data into a SQL Server database. It also generates a **data quality observability layer** for tracking dataset health across runs.

The pipeline is designed to simulate real-world production workflows used in retail analytics and data engineering systems.

---
<img width="3469" height="1827" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/1d0a8416-e776-4b4a-81d2-77df74b6f38e" />

## 🏗️ Architecture

```
Kaggle Dataset
      ↓
[Extractor] → Downloads raw data
      ↓
[Validator] → Structure + Quality checks
      ↓
[Data Quality Report] → Metrics tracking (nulls, duplicates, schema)
      ↓
[Transformer] → Cleaning + feature engineering
      ↓
[Loader] → SQL Server ingestion
      ↓
[Observability Layer] → Stores quality report in SQL
```

---

## 📦 Features

### 🔹 Data Ingestion

* Kaggle API-based dataset extraction
* Automatic dataset unpacking into raw layer

### 🔹 Data Validation

* Schema validation
* Null ratio detection
* Duplicate detection
* Column-level integrity checks

### 🔹 Data Quality Reporting

* Rows before/after tracking
* Null percentage per column
* Duplicate ratio
* Stored as structured JSON + SQL table

### 🔹 Data Transformation

* Feature engineering
* Cleaning pipeline (multi-dataset support)
* Standardized processed outputs

### 🔹 SQL Server Loading

* Bulk insert via `pandas.to_sql`
* SQL-safe type conversions (uint → int64)
* Column normalization
* Chunked loading for performance

### 🔹 Observability

* Run-level tracking (UUID per pipeline run)
* Data quality report persisted into SQL Server

---

## 🧱 Project Structure

```
retail-market-intelligence/
│
├── data/
│   ├── raw/
│   ├── processed/
│
├── logs/
│
├── src/
│   ├── extract/
│   ├── validate/
│   ├── transform/
│   ├── load/
│   ├── utils/
│
├── run.py
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run

### 1. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Set Kaggle Credentials

Place your Kaggle API token in:

```
C:\Users\<YOUR_USER>\.kaggle\kaggle.json
```

---

### 4. Run Pipeline

```bash
python -m run
```

---

## 🧪 Example Output

```
PIPELINE STARTED
STAGE 1: EXTRACTION COMPLETE
STAGE 2: VALIDATION COMPLETE
STAGE 3: TRANSFORMATION COMPLETE
STAGE 4: LOADING COMPLETE
PIPELINE SUCCESSFULLY COMPLETED
```

---

## 📊 Data Quality Metrics Stored

Each run captures:

| Metric          | Description                  |
| --------------- | ---------------------------- |
| rows_before     | Raw dataset size             |
| columns         | Number of columns            |
| null_ratio      | Percentage of missing values |
| duplicate_ratio | Percentage of duplicate rows |

Stored in:

```
SQL Server → data_quality_report table
```

---

## 🧠 Key Design Decisions

### 1. SQL Safety Layer

* Converted `uint64 → int64`
* Replaced NaN → NULL
* Disabled unsafe bulk insert methods when needed

### 2. Observability First Design

* Every pipeline run has a UUID
* Data quality tracked independently from transformation

### 3. Multi-Dataset Architecture

* Pipeline supports multiple CSV datasets in one run

---

## ⚠️ Known Issues / Fixes Applied

### ✔ SQL Server 07002 Error

Fixed by:

* Removing `method="multi"` in some cases
* Sanitizing numeric types before load

### ✔ Unsigned Integer Crash

Fixed by:

* Converting `uint64 → int64`

### ✔ Empty Data Quality Table

Fixed by:

* Ensuring `report_df` is returned from validator
* Ensuring pipeline passes DataFrame into SQL writer

---

## 📈 Future Improvements

* Add Airflow orchestration
* Add S3 / cloud storage support
* Add dbt transformations layer
* Add Power BI / dashboard integration
* Add anomaly detection in validation stage
* Add incremental loading strategy

---

## 👨‍💻 Author

**Tembinkosi Vikani Dube**
Data Engineer | Data Analytics | Process Improvement

GitHub:
[https://github.com/tembinkosid-bit/Data-Analytics-Portfolio](https://github.com/tembinkosid-bit/Data-Analytics-Portfolio)

LinkedIn:
[https://www.linkedin.com/in/tembinkosi-vikani-dube/](https://www.linkedin.com/in/tembinkosi-vikani-dube/)

---

## 📌 License

This project is for educational and portfolio purposes.

---
