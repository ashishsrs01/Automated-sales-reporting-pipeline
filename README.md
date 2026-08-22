# Automated Sales Reporting Pipeline

> A production-style Python pipeline that transforms raw sales data into validated analytics, business insights, actionable recommendations, and an automated executive HTML dashboard.

![Python](https://img.shields.io/badge/Python-3.13+-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-3.0.1-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-2.4.3-013243?logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.x-11557C?logo=matplotlib&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-69%20passed-success)
![Ruff](https://img.shields.io/badge/Code%20Quality-Ruff-D7FF64)
![License](https://img.shields.io/badge/License-MIT-blue)

## Dashboard Preview

![Executive Sales Dashboard](docs\images\dashboard-preview.png)

### Key Results

- **69 automated tests** passing
- **End-to-end automated reporting pipeline**
- **Executive HTML dashboard** generated from raw sales data
- **Automated business insights and recommendations**
- **Data-quality monitoring and validation**
- **Reproducible project configuration** with `pyproject.toml`

---

## 📊 Overview

**Automated Sales Reporting Pipeline** is an end-to-end analytics project designed to automate the process of turning raw transactional sales data into a business-ready executive report.

Instead of manually cleaning spreadsheets, calculating KPIs, creating charts, and writing observations, the pipeline performs the complete workflow programmatically.

### The pipeline

```text
Raw Sales Data
      ↓
Data Ingestion
      ↓
Data Validation & Quality Checks
      ↓
Data Cleaning
      ↓
KPI & Business Analytics
      ↓
Time-Series Analysis
      ↓
Business Insights
      ↓
Actionable Recommendations
      ↓
Automated Charts
      ↓
Executive HTML Dashboard
```

The project demonstrates how a data analyst can build a **repeatable and maintainable reporting workflow** rather than producing a one-off analysis.

---

## 🎯 Business Objective

The goal is to answer practical business questions such as:

* How much revenue was generated?
* How many orders were processed?
* What is the average order value?
* Which regions generate the most revenue?
* Which product categories perform best?
* Which products and salespeople contribute most?
* Where are significant month-over-month changes occurring?
* Are there data-quality issues that could affect business decisions?
* What actions should management investigate next?

The final report is designed around the principle:

> **Metrics → Key Findings → Risk → Evidence → Recommended Action**

---

## ✨ Key Features

### Data Engineering

* CSV-based data ingestion
* Schema and data-quality validation
* Missing-value handling
* Duplicate-order detection and removal
* Date normalization
* Numeric/data-type validation
* Clean transformation pipeline

### Analytics

* Revenue analysis
* Order-volume analysis
* Average Order Value (AOV)
* Monthly revenue trends
* Month-over-month growth
* Regional performance
* Category performance
* Product performance
* Salesperson performance

### Business Intelligence

* Automated KPI calculation
* Identification of top-performing dimensions
* Detection of abnormal revenue changes
* Data-quality impact analysis
* Automated business insights
* Action-oriented recommendations

### Reporting

* Automatically generated charts
* Executive-style HTML dashboard
* Business-friendly financial formatting
* Revenue anomaly/risk communication
* Responsive dashboard layout
* Automated report generation from processed data

### Engineering Quality

* Modular Python architecture
* Automated test suite
* 69 passing tests
* Ruff linting
* Ruff formatting
* Centralized project configuration through `pyproject.toml`

---

## 🖥️ Executive Dashboard

The final dashboard is designed to communicate the most important information quickly.

### Dashboard structure

```text
┌─────────────────────────────────────────────────────────┐
│                 SALES PERFORMANCE                       │
├─────────────┬─────────────┬─────────────┬───────────────┤
│   REVENUE   │   ORDERS    │     AOV     │   MOM GROWTH  │
├──────────────────────────────────┬──────────────────────┤
│                                 │                      │
│         REVENUE TREND           │ EXECUTIVE SNAPSHOT   │
│                                 │                      │
├──────────────────────┬──────────┴──────────────────────┤
│ Revenue by Region    │ Revenue by Category             │
├──────────────────────┴─────────────────────────────────┤
│ Top Products                         │ Salesperson      │
├────────────────────────────────────────────────────────┤
│ ⚠ Business Risk / Revenue Alert                       │
├──────────────────────────────┬─────────────────────────┤
│ Recommended Actions          │ Data Quality             │
└──────────────────────────────┴─────────────────────────┘
```

The dashboard prioritizes:

1. **Overall business performance**
2. **Important changes and risks**
3. **Supporting evidence**
4. **Recommended actions**
5. **Data-quality visibility**

---

## 🚨 Example Business Finding

The pipeline is capable of identifying significant changes in business performance and turning them into actionable investigation points.

For example, the generated report identified a substantial latest-month revenue decline and surfaced the issue as an executive risk rather than simply displaying it on a chart.

The report then recommends actions such as:

* Compare the latest month against the previous month by region.
* Identify categories and products contributing to the decline.
* Verify source-data completeness for the latest reporting period.

This distinction is important:

> The project doesn't stop at **"what happened?"**

It progresses toward:

> **"What happened, why should we care, and what should we investigate next?"**

---

## 🧹 Data Quality Intelligence

Data-quality problems are treated as business problems rather than being silently hidden.

The dashboard exposes unknown or missing dimensions and quantifies their impact.

For example, the final report surfaced revenue associated with unknown:

* Categories
* Regions
* Salespeople

This allows a business user to investigate affected records and improve the underlying reporting data.

---

## 🏗️ Project Structure

```text
Automated-sales-reporting-pipeline/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── reports/
│   └── business-performance-report.html
│
├── src/
│   └── reporting/
│       ├── __init__.py
│       ├── aggregations.py
│       ├── charts.py
│       ├── dates.py
│       ├── duplicates.py
│       ├── insights.py
│       ├── missing.py
│       ├── pipeline.py
│       ├── validation.py
│       └── html.py
│
├── tests/
│   ├── ...
│
├── run.py
├── pyproject.toml
├── README.md
└── .gitignore
```

The architecture separates:

* Data preparation
* Validation
* Business calculations
* Insight generation
* Visualization
* Report rendering

This makes individual components easier to test and maintain.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/ashishsrs01/Automated-sales-reporting-pipeline.git
cd Automated-sales-reporting-pipeline
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install the project

```bash
pip install -e .
```

For development/testing dependencies:

```bash
pip install -e ".[dev]"
```

---

## ▶️ Running the Pipeline

From the project root:

```bash
python run.py
```

The pipeline processes the available sales data and generates the executive HTML report.

The generated report is written to:

```text
reports/business-performance-report.html
```

Open the HTML file in a browser to view the dashboard.

---

## 🧪 Testing

The project includes a comprehensive automated test suite.

Run:

```bash
python -m pytest
```

Current validation:

```text
69 tests passed
```

---

## 🔍 Code Quality

Ruff is used for linting and formatting.

Run lint checks:

```bash
python -m ruff check .
```

Check formatting:

```bash
python -m ruff format --check .
```

Automatically format the project:

```bash
python -m ruff format .
```

---

## 📦 Dependencies

### Runtime

* Python 3.13+
* pandas
* numpy
* matplotlib

### Development

* pytest
* ruff

Dependencies are declared in:

```text
pyproject.toml
```

This keeps the project environment reproducible instead of depending on a machine-specific `pip freeze`.

---

## 🧠 Skills Demonstrated

This project demonstrates practical experience with:

### Python

* Modular Python development
* Functions and reusable components
* File I/O
* Data transformation
* Error handling
* Project organization

### Data Analysis

* pandas
* NumPy
* Aggregations
* Group-by analysis
* Time-series analysis
* KPI development
* Business metrics

### Data Quality

* Missing-value analysis
* Duplicate detection
* Type validation
* Date normalization
* Data-quality reporting

### Data Visualization

* Matplotlib
* Business-oriented chart design
* KPI visualization
* Trend analysis
* Anomaly communication
* Executive dashboard design

### Software Engineering

* Automated testing
* pytest
* Ruff
* Configuration management
* Modular architecture
* Reproducible environments

### Business Analytics

* Performance analysis
* Root-cause investigation
* Risk identification
* Insight generation
* Actionable recommendations
* Executive reporting

---

## 💼 Freelancing Use Case

This project represents a realistic service that can be offered to businesses handling recurring spreadsheet or CSV-based reports.

A client could provide:

```text
Monthly Sales CSV / Excel Export
             ↓
      Automated Pipeline
             ↓
 ┌───────────────────────────┐
 │ Data Cleaning             │
 │ Validation                │
 │ KPI Calculation           │
 │ Trend Analysis            │
 │ Business Insights         │
 │ Recommendations           │
 └───────────────────────────┘
             ↓
     Executive Dashboard
             ↓
       HTML Report
```

Instead of manually preparing the same report every month, the workflow can be rerun against updated data.

Potential client applications include:

* Sales reporting
* Operations reporting
* Revenue analysis
* Performance monitoring
* Management dashboards
* Recurring business reports
* Data-quality monitoring

---

## 📈 Why This Project Matters

A typical beginner analytics project might demonstrate:

> "I can make charts from a dataset."

This project demonstrates a broader workflow:

> **"I can build an automated reporting system that turns raw business data into validated metrics, insights, recommendations, and an executive-facing deliverable."**

That difference is the main purpose of the project.

---

## 🔮 Future Improvements

Possible future extensions include:

* Excel input support
* Database connectivity
* Scheduled report generation
* Email delivery of reports
* Configurable KPI definitions
* Multiple client/report templates
* Interactive filtering
* Cloud deployment
* Automated data ingestion from business systems
* PDF report generation
* Report history and trend tracking

These are intentionally outside the current core scope so that the existing pipeline remains focused and maintainable.

---

## 📋 Validation Status

| Component              | Status  |
| ---------------------- | ------- |
| Data ingestion         | ✅       |
| Data validation        | ✅       |
| Data cleaning          | ✅       |
| Duplicate handling     | ✅       |
| Date normalization     | ✅       |
| KPI analytics          | ✅       |
| Time-series analysis   | ✅       |
| Business insights      | ✅       |
| Recommendations        | ✅       |
| Automated charts       | ✅       |
| Executive dashboard    | ✅       |
| HTML report generation | ✅       |
| Automated tests        | ✅ 69/69 |
| Ruff linting           | ✅       |
| Ruff formatting        | ✅       |
| Project configuration  | ✅       |

---

## 👤 Author

**Ashish Sharma**

AI & Data Science Student
Focused on **Data Analytics, AI/ML, and Analytics Engineering**

GitHub: `https://github.com/ashishsrs01`

---

## 📄 License

This project is licensed under the MIT License.
