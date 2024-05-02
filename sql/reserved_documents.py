from sql.db import DB
from tabulate import tabulate

def get_reserved_documents():
    try:
        # Connect to the database
        db = DB()

        # SQL query to select all reserved documents
        query = "SELECT * FROM RESERVED_DOCUMENTS;"
        result = db.selectAll(query)

        # Check if the query was successful
        if result.status:
            reserved_documents = result.rows
            return reserved_documents
        else:
            print("Error retrieving reserved documents.")

    except Exception as e:
        print("An error occurred:", e)

    finally:
        try:
            # Close the database connection
            db.close()
        except Exception as ce:
            print("An error occurred while closing the cursor:", ce)

if __name__ == "__main__":
    # Call the function to get all reserved documents
    reserved_documents = get_reserved_documents()
    if reserved_documents:
        headers = reserved_documents[0].keys()
        rows = [doc.values() for doc in reserved_documents]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        print("No reserved documents found.")
