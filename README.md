# DatabaseAI Project

## System Overview

This project implements a simplified AI-assisted database system using Python and SQLite.

The system supports:

* Loading CSV files into a database
* Automatic schema inference
* SQL query validation (security layer)
* Controlled query execution
* Command-line interface (CLI)

### Architecture

CLI → QueryService → SQLValidator → Database
↑
SchemaManager
↑
CSVLoader

---

## How to Run the Project

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the CLI

```bash
python -m app.cli
```

### 3. Example usage

```text
> load data/sample.csv sales
> tables
> schema sales
> query SELECT * FROM sales;
```

---

## How to Run Tests

```bash
pytest
```

---

## Features

### CSV Loader

* Uses pandas to read CSV files
* Automatically creates database tables
* Infers schema from data types

### Schema Manager

* Normalizes column names
* Tracks table schemas
* Ensures consistency across queries

### SQL Validator (Security Layer)

* Only allows SELECT queries
* Blocks dangerous operations (DELETE, DROP, UPDATE, etc.)
* Prevents SQL injection
* Validates table existence

### Query Service

* Central query execution layer
* Ensures validation before execution
* Returns structured results

### CLI Interface

Available commands:

```text
load <csv_path> <table_name>
tables
schema <table_name>
query <SQL>
exit
```

---

## Project Structure

```
app/
    db.py
    csv_loader.py
    schema_manager.py
    validator.py
    query_service.py
    cli.py
tests/
data/
.github/workflows/
```

---

## Notes

* SQLite is used as the database backend
* pandas is used only for CSV ingestion
* All SQL queries are validated before execution for security
