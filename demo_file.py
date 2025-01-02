from flask import Flask, render_template, request, jsonify, send_file
import pyodbc
import json
import os

app = Flask(__name__)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle schema generation for SQL Server
@app.route('/generate-schema', methods=['POST'])
def generate_schema():
    data = request.json
    db_type = data.get("db_type")  # SQL Server
    host = data.get("host")
    database = data.get("database")
    username = data.get("username")
    password = data.get("password")

    if not all([host, database, username, password, db_type]):
        return jsonify({"success": False, "error": "All fields are required"}), 400

    if db_type != 'sqlserver':
        return jsonify({"success": False, "error": "Unsupported database type, only SQL Server is supported"}), 400

    try:
        # Connect to SQL Server
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={host};DATABASE={database};UID={username};PWD={password}"
        )

        # Extract schema information
        cursor = conn.cursor()
        tables = {}

        # Get table columns for SQL Server
        cursor.execute(""" 
            SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE 
            FROM INFORMATION_SCHEMA.COLUMNS 
        """)

        for row in cursor.fetchall():
            table_name = row[0]
            column_name = row[1]
            data_type = row[2]

            if table_name not in tables:
                tables[table_name] = {"columns": [], "primary_keys": [], "foreign_keys": []}

            tables[table_name]["columns"].append(f"{column_name} ({data_type})")

        # Fetch primary keys for SQL Server
        cursor.execute(""" 
            SELECT 
                kcu.TABLE_NAME, kcu.COLUMN_NAME, c.DATA_TYPE 
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu 
            JOIN INFORMATION_SCHEMA.COLUMNS c 
                ON kcu.TABLE_NAME = c.TABLE_NAME AND kcu.COLUMN_NAME = c.COLUMN_NAME 
            WHERE OBJECTPROPERTY(OBJECT_ID(kcu.CONSTRAINT_NAME), 'IsPrimaryKey') = 1
        """)

        for row in cursor.fetchall():
            table_name = row[0]
            column_name = row[1]
            data_type = row[2]

            if table_name in tables:
                tables[table_name]["primary_keys"].append(f"{column_name} ({data_type})")

        # Fetch foreign keys for SQL Server
        cursor.execute(""" 
            SELECT 
                fk.TABLE_NAME, cu.COLUMN_NAME, pk.TABLE_NAME AS REFERENCED_TABLE_NAME, 
                pt.COLUMN_NAME AS REFERENCED_COLUMN_NAME, c.DATA_TYPE 
            FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS rc 
            JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS fk 
                ON rc.CONSTRAINT_NAME = fk.CONSTRAINT_NAME 
            JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS pk 
                ON rc.UNIQUE_CONSTRAINT_NAME = pk.CONSTRAINT_NAME 
            JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE cu 
                ON fk.CONSTRAINT_NAME = cu.CONSTRAINT_NAME 
            JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE pt 
                ON pk.CONSTRAINT_NAME = pt.CONSTRAINT_NAME 
            JOIN INFORMATION_SCHEMA.COLUMNS c 
                ON fk.TABLE_NAME = c.TABLE_NAME AND cu.COLUMN_NAME = c.COLUMN_NAME 
        """)

        for row in cursor.fetchall():
            table_name = row.TABLE_NAME
            column_name = row.COLUMN_NAME
            referenced_table = row.REFERENCED_TABLE_NAME
            referenced_column = row.REFERENCED_COLUMN_NAME
            data_type = row.DATA_TYPE

            if table_name in tables:
                tables[table_name]["foreign_keys"].append({
                    "column": f"{column_name} ({data_type})",
                    "references": {
                        "table": referenced_table,
                        "column": referenced_column
                    }
                })

        # Save schema to JSON file
        schema_file = 'database_schema.json'
        with open(schema_file, 'w') as f:
            json.dump(tables, f, indent=4)

        conn.close()
        return jsonify({"success": True, "file_url": '/download-schema'})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Route for downloading the generated schema
@app.route('/download-schema', methods=['GET'])
def download_schema():
    file_path = 'database_schema.json'
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({"success": False, "error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True,port=5001)
