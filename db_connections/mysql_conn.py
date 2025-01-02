import mysql.connector

def generate_mysql_schema(host, username, password, database, port=3306):
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database,
            port=port
        )
        cursor = conn.cursor()

        try:
            # Query to get all tables in the database
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            schema = {}

            for table in tables:
                table_name = table[0]
                table_info = {
                    "columns": [],
                    "primary_keys": [],
                    "foreign_keys": []
                }

                try:
                    # Get columns for the table and store column types in a dictionary
                    cursor.execute(f"DESCRIBE {table_name}")
                    columns = cursor.fetchall()
                    column_types = {column[0]: column[1] for column in columns}  # Column names with their data types

                    for column in columns:
                        column_info = f"{column[0]} ({column[1]})"
                        table_info["columns"].append(column_info)

                        # Collect primary keys (only 'PRI' columns)
                        if column[3] == 'PRI':
                            table_info["primary_keys"].append(f"{column[0]} ({column[1]})")

                    # Fetch foreign keys for the table
                    cursor.execute(f"""
                        SELECT CONSTRAINT_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
                        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                        WHERE TABLE_NAME = '{table_name}' AND TABLE_SCHEMA = '{database}'
                        AND REFERENCED_TABLE_NAME IS NOT NULL
                    """)
                    foreign_keys = cursor.fetchall()

                    for fk in foreign_keys:
                        # Use the column name to get its data type from the column_types dictionary
                        column_name = fk[1]
                        data_type = column_types.get(column_name, "unknown")

                        foreign_key_info = {
                            "column": f"{column_name} ({data_type})",
                            "references": {
                                "table": fk[2],
                                "column": fk[3]
                            }
                        }
                        table_info["foreign_keys"].append(foreign_key_info)

                    schema[table_name] = table_info

                except mysql.connector.Error as err:
                    print(f"Error retrieving columns or foreign keys for table {table_name}: {err}")
                    continue

            return schema
        
        except mysql.connector.Error as err:
            print(f"Error executing SHOW TABLES or fetching table list: {err}")
            return {}

        finally:
            cursor.close()
            conn.close()

    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        return {}

