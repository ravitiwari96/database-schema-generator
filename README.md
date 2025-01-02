## Database Schema Generator
  This tool allows you to easily generate the schema of your database in JSON format. It supports PostgreSQL, MySQL, and SQL Server. Simply input your database credentials,    click the "Generate Schema" button, and download the JSON schema file for your database.

## Features
  - Supports PostgreSQL, MySQL, and SQL Server.
  - Input your database credentials (host, user, password, and database name).
  - Click the "Generate Schema" button to automatically generate the schema.
  - Download the schema in JSON format.
  - Simple and intuitive user interface for easy access.

## Requirements
  - Python 3.x
  - Required libraries are included in the **requirements.txt** file.

## Installation and Setup
**Step 1:** Create a Virtual Environment
            It's recommended to set up a virtual environment to avoid package conflicts.
            
            python -m venv venv
            
**Step 2:** Install Required Libraries
            Activate your virtual environment and install the necessary dependencies:
            
            venv\Scripts\activate
            pip install -r requirements.txt

**Step 3:** Running the Application
            Run the application by executing the following command:
            
            python app.py
          
**Step 4:** Accessing the User Interface
    After running the app.py, a user interface will be available where you can:
  - Enter the credentials for your database (host, username, password, and database name).
  - Click the "Generate Schema" button.
  - The schema will be automatically generated, and you can download it in JSON format.

## Supported Databases
  - PostgreSQL
  - MySQL
  - SQL Server


<img width="725" alt="image" src="https://github.com/user-attachments/assets/e81aea87-7bef-413f-a5a9-8a503b53573a" />


## How It Works
  - You input the necessary database credentials.
  - The tool connects to your database, retrieves the schema, and converts it into a JSON format.
  - You can download the schema as a file once the process is complete.
