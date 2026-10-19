# ISVASA Studio – Embroidery Order Management & ETL Pipeline

**Manage • Create • Personalise**

## Project Overview

ISVASA Studio is a Python-based order management application designed to process manually exported e-commerce order data and convert it into a structured, reporting-friendly format.

The project demonstrates an end-to-end ETL (Extract, Transform, Load) workflow, including CSV ingestion, data cleaning, column standardisation, transformation, structured data preparation, and dashboard-based reporting using Streamlit.

It addresses the challenge of working with raw e-commerce order exports, where customer details, product information, and personalisation requirements need to be organised for operational tracking and reporting.

## Project Objectives

- Build a reusable workflow for ingesting e-commerce order data from CSV files.
- Transform raw source data into structured and usable business fields.
- Organise order and personalisation information for operational processing.
- Prepare data for reporting and dashboard analysis.
- Develop a simple user interface for uploading files and reviewing processed orders.

## ETL Workflow

**1. Extract**
- Ingest manually exported e-commerce order CSV files through the application.
- Read source fields containing order details, buyer information, product attributes, and personalisation instructions.

**2. Transform**
- Standardise source column names and map source fields to a consistent order structure.
- Organise order and customer information into usable fields.
- Extract and structure relevant personalisation details, such as embroidered names, initials, thread colours, fonts, and custom text, where available in the source data.
- Prepare the transformed records for operational review and reporting.

**3. Load / Prepare for Reporting**
- Structure the transformed order records into a consistent master-order format.
- Make processed order information available through the application's order management and reporting interface.
- Support review and tracking of order details and production-related statuses.

*Note: The persistence layer and exact load destination depend on the current application implementation.*

## Technology Stack

- **Language:** Python
- **Application Framework:** Streamlit
- **Data Ingestion:** CSV files
- **Data Transformation:** Python and Pandas, where used in the implementation
- **Version Control:** Git and GitHub

## Application Features

- CSV upload interface for manually exported e-commerce orders.
- Structured order data with standardised business fields.
- Order and personalisation information management.
- Dashboard for reviewing order information.
- Foundation for tracking production, design, and customisation statuses.

## Data Structure

The target order structure is designed to accommodate fields such as:

| Category | Example fields |
|---|---|
| Order details | Order ID, transaction ID, order date |
| Customer details | Buyer, recipient |
| Product details | Product category, product title, quantity, colour |
| Personalisation | Embroidered name, initials, thread colour, font, custom text |
| Workflow tracking | Customisation status, production status, image status, tracing status |

Actual fields populated depend on the source CSV and the implemented transformation logic.

## Project Architecture

```text
Manually Exported E-commerce CSV
              |
              v
     Streamlit Upload Interface
              |
              v
       Extract Source Data
              |
              v
     Validate and Transform
              |
              v
   Standardised Order Records
              |
              v
     Order Management Views
              |
              v
       Dashboard & Reporting
```

## How to Run Locally

### Prerequisites
- Python installed
- Git installed
- Visual Studio Code or another code editor

### 1. Clone the repository

```bash
git clone https://github.com/swetasivani1-arch/isvasa-studio.git
cd isvasa-studio
```

### 2. Create and activate a virtual environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

If a `requirements.txt` file is included:

```bash
pip install -r requirements.txt
```

### 4. Start the Streamlit application

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal.

## Data Privacy

The application is designed around manually exported CSV files rather than automatic Etsy API integration. Use sample or anonymised order data when demonstrating the project publicly. Do not commit real customer information, credentials, API keys, or environment files to GitHub.

## Skills Demonstrated

- ETL pipeline design and implementation
- File-based data ingestion
- Data cleaning and transformation
- Source-to-target field mapping
- Structured data preparation for reporting
- Python application development
- Dashboard development with Streamlit
- Git-based version control

## Future Enhancements

- Add automated data-quality checks and validation reports.
- Introduce a persistent relational database for order storage.
- Implement incremental loading and duplicate-order handling.
- Add automated ETL execution logs and error handling.
- Expand dashboard metrics and operational reporting.
- Add unit tests for transformation and validation logic.

## Repository

GitHub: https://github.com/swetasivani1-arch/isvasa-studio

**Author:** Sweta Shivani

*This project is a practical demonstration of applying data engineering concepts to an e-commerce order management use case.*