import pyodbc

def generate_sqlserver_schema(host, username, password, database):
    try:
        # Connect to SQL Server
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={host};DATABASE={database};UID={username};PWD={password}"
        )
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return {}

    cursor = conn.cursor()
    tables = {}

    try:
        # Fetch table columns
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

        # Fetch primary keys
        cursor.execute(""" 
            SELECT kcu.TABLE_NAME, kcu.COLUMN_NAME, c.DATA_TYPE 
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

        # Fetch foreign keys
        cursor.execute(""" 
            SELECT fk.TABLE_NAME, cu.COLUMN_NAME, pk.TABLE_NAME AS REFERENCED_TABLE_NAME, 
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
    except Exception as err:
        print(f"Error while fetching schema data: {err}")
    finally:
        # Close the connection after operations
        conn.close()

    return tables
