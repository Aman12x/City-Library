from sql.db import DB

def retrieve_branch_info(branch_id):
    # SQL query to retrieve branch information
    sql_query = f"""
        SELECT BNAME, BLOCATION
        FROM BRANCH
        WHERE BID = '{branch_id}';
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

# Take user input for branch ID
branch_id = input("Enter the branch ID: ")

# Call the function with user input
result = retrieve_branch_info(branch_id)

if result:
    print("Branch information for branch ID", branch_id, ":", result)
else:
    print("No branch found with ID", branch_id)
