# Finance Data Dashboard

## Project Overview

This project is a finance analytics dashboard built using SQL, SQLite, Python, and Streamlit.

The goal of this project is to demonstrate an end-to-end analytics workflow, starting from raw CSV files, importing and cleaning data in SQLite, creating SQL views for analysis, and building an interactive dashboard in Streamlit.

This project focuses on analyzing invoice, vendor, budget, and workforce-related data in a structured dashboard format.


## Objective

The main objective of this project is to create a dashboard that helps users monitor key finance and operational metrics, including:

- Total invoice amount
- Outstanding vendor balances
- Invoice status by client
- Overdue and pending invoice balances
- Budget versus actual analysis
- Workforce and department-level cost insights


## Tools and Technologies

- SQL
- SQLite
- DB Browser for SQLite
- Python
- Pandas
- Streamlit
- Plotly
- Git
- GitHub


## Project Structure

```text
finance_data_dashboard_project/
│
├── raw_data/              # Original CSV files
├── cleaned_data/          # Cleaned CSV files
├── database/              # SQLite database file
├── sql/                   # SQL scripts for cleaning, transformation, and views
├── app/                   # Streamlit dashboard application
├── notebooks/             # Python ipynb files
└── README.md              # Project documentation
```

## Data Preparation

This project uses a combination of raw CSV files and synthetic data created for portfolio purposes.

The raw CSV files were prepared before importing them into SQLite. 
For the budget dataset, I created a synthetic budget CSV using Python so that the dashboard could include budget versus actual analysis without using confidential company budget data.

The data preparation process included:

- Reviewing the original raw CSV files
- Cleaning and standardizing column names
- Handling missing or inconsistent values
- Creating a synthetic budget dataset using Python
- Exporting cleaned files as CSV

## Data Workflow

The workflow for this project follows a typical analytics pipeline:

```text
Raw CSV Files
↓
Python Data Cleaning and Synthetic Budget Data Creation
↓
SQLite Database
↓
Data Transformation/ SQL Views for Dashboard Analysis
↓
Streamlit Dashboard
```


## SQL Process

The raw CSV files were imported into SQLite tables. SQL was then used to check, transform, and summarize the data.

Examples of SQL work completed in this project include:

- Creating cleaned tables
- Aggregating invoice balances by client and invoice status
- Creating dashboard-ready SQL views
- Calculating total outstanding balances using grouped queries and window functions


## Key SQL Views

The dashboard uses SQL views to simplify the analysis layer.

Examples of views used in this project include:

- `company_status_summary`
- `vendor_balance_summary`
- `monthly_invoice_trend`
- `budget_vs_actual_summary`
- `department_workforce_summary`

These views help separate the data preparation logic from the dashboard code.


## Dashboard Features

The Streamlit dashboard includes:

- KPI cards for total invoice amount, outstanding balance, and invoice count
- Client/vendor filters
- Outstanding balance by client
- Invoice status breakdown
- Top vendors by outstanding balance
- Budget versus actual charts
- Interactive data tables


## Business Value

This dashboard helps finance and operations teams quickly understand invoice exposure, outstanding balances, vendor payment status, and budget performance.

Instead of reviewing multiple CSV files manually, users can view summarized metrics and interactive charts in one place.


## Skills Demonstrated

This project demonstrates the following skills:

- SQL data cleaning and transformation
- SQLite database management
- Creating reusable SQL views
- Window functions and aggregation
- Python data analysis with Pandas
- Dashboard development with Streamlit
- Data visualization with Plotly
- Git and GitHub project documentation


## Disclaimer

This project uses sample and synthetic data for portfolio purposes. No confidential company information is included.
