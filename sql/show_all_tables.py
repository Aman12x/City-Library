from tabulate import tabulate
from sql.db import DB
def show_table(table_name):
    try:
        # SQL query to retrieve all rows from the specified table
        query = f"SELECT * FROM {table_name};"

        # Execute the SQL query to fetch all rows from the specified table
        response = DB.selectAll(query)

        if response.status:
            # Display the rows of the specified table in a table format
            print(f"Contents of table '{table_name}':")
            headers = response.rows[0].keys() if response.rows else []
            rows = [list(row.values()) for row in response.rows]
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        else:
            print(f"Error: Unable to fetch rows from table '{table_name}'")

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    # Prompt the user to enter the table name
    table_name = input("Enter the name of the table you want to view: ")

    # Call the function to show the specified table
    show_table(table_name)
