from sql.db import DB

def get_reader_name(reader_id):
    # SQL query to retrieve reader name
    sql_query = f"""
        SELECT RNAME
        FROM READER
        WHERE RID = '{reader_id}';
    """

    # Execute the SQL query using the DB class
    response = DB.selectAll(sql_query)

    # Check if the query was successful
    if response.status:
        # If successful, return the result rows
        return response.rows
    else:
        # If not successful, print an error message
        print("Error executing SQL query")

# Take user input for reader ID
reader_id = input("Enter the reader ID: ")

# Call the function with user input
result = get_reader_name(reader_id)

if result:
    print("Reader exists", reader_id, ":", result)
else:
    print("No reader found", reader_id)
