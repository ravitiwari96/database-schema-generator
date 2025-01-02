## SCHEMAGENERATOR/
├──db_connections
|   ├──mysql_conn.py
|   ├──postgresql_conn.py
|   ├──sqlserver_conn.py 
├── app.py                  # Main Flask application
├── templates/
│   ├── index.html          # HTML for the user interface
├── database_schema.json    # Generated schema file (output)
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation







## Database Schema Generator

    This project provides a Python-based tool to generate the schema of any database (MySQL, PostgreSQL, SQL Server). The schema includes table columns, primary keys, and foreign keys, and outputs the information in a structured format.

## Features
    Connects to multiple databases: MySQL, PostgreSQL, SQL Server.
    Extracts schema information:
       - Table names
       - Columns and their data types
       - Primary keys
       - Foreign keys
       - Generates schema in a readable format for each database.
       - Exception handling for database connection errors.

## Supported Databases
    - MySQL
    - PostgreSQL
    - SQL Server

## Requirements
    Ensure you have the following Python libraries installed before running the code:
       - Python 
       - Flask 
       - mysql-connector-python (for MySQL)
       - psycopg (for PostgreSQL)
       - pyodbc (for SQL Server)
