from sql.db import DB

def clear_database():
    try:
        # Connect to the database
        db = DB()

        # SQL query to get all table names
        get_tables_query = "SHOW TABLES;"
        tables_result = db.selectAll(get_tables_query)

        if tables_result.status and tables_result.rows:
            for row in tables_result.rows:
                table_name = row['Tables_in_your_database_name']  # Replace with your actual database name
                drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
                drop_result = db.query(drop_table_query)
                if drop_result.status:
                    print(f"Table {table_name} dropped successfully.")
                else:
                    print(f"Error dropping table {table_name}.")

        else:
            print("No tables found in the database.")

    except Exception as e:
        print("An error occurred:", e)

    finally:
        try:
            # Close the database connection
            db.close()
        except Exception as ce:
            print("An error occurred while closing the connection:", ce)

if __name__ == "__main__":
    # Call the function to clear the database
    clear_database()
