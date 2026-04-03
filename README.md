# DatabaseAI Project

## Overview
This project implements a simplified AI-assisted database system using Python and SQLite.

It supports:
- Loading CSV files into a database
- Automatic schema inference
- SQL query validation
- Secure query execution
- Command-line interface (CLI)

---

## Features

### 1. CSV Loader
- Loads CSV files using pandas
- Automatically creates database tables
- Infers schema from data

### 2. Schema Manager
- Normalizes column names
- Tracks existing tables
- Validates schema compatibility

### 3. SQL Validator (Security Layer)
- Only allows SELECT queries
- Blocks dangerous commands (DROP, DELETE, etc.)
- Prevents SQL injection
- Ensures referenced tables exist

### 4. Query Service
- Central execution layer
- Validates queries before execution
- Returns structured results

### 5. CLI Interface
Commands:

load <csv_path> <table_name>
tables
schema <table_name>
query <SQL>
exit


---

## Installation

```bash
pip install -r requirements.txt
Usage

Run CLI:

python -m app.cli

Example:

> load data/sample.csv sales
> tables
> schema sales
> query SELECT * FROM sales;
Testing

Run tests:

pytest
Project Structure
app/
    db.py
    csv_loader.py
    schema_manager.py
    validator.py
    query_service.py
    cli.py
tests/
data/
Notes
pandas is only used for CSV reading
SQLite is used for storage
SQL execution is strictly validated

---

