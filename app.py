from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from db_connections import mysql_conn, postgresql_conn, sqlserver_conn


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-schema', methods=['POST'])
def generate_schema():
    data = request.json
    db_type = data.get("db_type")  # MySQL, SQL Server, or PostgreSQL
    host = data.get("host")
    database = data.get("database")
    username = data.get("username")
    password = data.get("password")

    if not all([host, database, username, password, db_type]):
        return jsonify({"success": False, "error": "All fields are required"}), 400

    try:
        if db_type == 'mysql':
            schema = mysql_conn.generate_mysql_schema(host, username, password, database)
        elif db_type == 'postgresql':
            schema = postgresql_conn.generate_postgresql_schema(host, username, password, database)
        elif db_type == 'sqlserver':
            schema = sqlserver_conn.generate_sqlserver_schema(host, username, password, database)
        else:
            return jsonify({"success": False, "error": "Unsupported database type"}), 400

        # Save schema to JSON file
        schema_file = 'database_schema.json'
        with open(schema_file, 'w') as f:
            json.dump(schema, f, indent=4)

        return jsonify({"success": True, "file_url": '/download-schema'})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/download-schema', methods=['GET'])
def download_schema():
    file_path = 'database_schema.json'
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({"success": False, "error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
