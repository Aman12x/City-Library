from sql.db import DB  # Import the DB class from db.py

def return_reserved_document(reader_id=None, doc_id=None):
    """
    Function to remove reserved document entries from the database.
    """
    try:
        # Connect to the database
        db = DB()

        # Construct the WHERE clause based on the provided reader_id and doc_id
        where_clause = ""
        if reader_id is not None and doc_id is not None:
            where_clause = f"WHERE RID = {reader_id} AND DOCID = {doc_id}"
        elif reader_id is not None:
            where_clause = f"WHERE RID = {reader_id}"
        elif doc_id is not None:
            where_clause = f"WHERE DOCID = {doc_id}"

        # SQL query to delete reserved document entry/entries
        query = f"""
        DELETE FROM RESERVED_DOCUMENTS
        {where_clause};
        """
        
        # Execute the SQL query
        result = db.query(query)

        # Check if the query was successful
        if result.status:
            if reader_id is not None and doc_id is not None:
                print("Reserved document returned successfully.")
            elif reader_id is not None:
                print("All reserved documents for the specified reader returned successfully.")
            elif doc_id is not None:
                print("All reserved documents for the specified document returned successfully.")
        else:
            print("Error returning reserved document(s).")

    except Exception as e:
        print("An error occurred:", e)

    finally:
        try:
            # Close the database connection
            db.close()
        except Exception as ce:
            print("An error occurred while closing the cursor:", ce)

if __name__ == "__main__":
    # Example usage: take user input for reader ID and document ID
    reader_id = input("Enter the reader ID (press Enter to skip): ")
    doc_id = input("Enter the document ID (press Enter to skip): ")

    # Convert input to integers if not empty
    reader_id = int(reader_id) if reader_id else None
    doc_id = int(doc_id) if doc_id else None

    # Call the function to return reserved document(s)
    return_reserved_document(reader_id, doc_id)