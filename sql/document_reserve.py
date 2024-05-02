from sql.db import DB  # Import the DB class from db.py

def store_reserved_document(reader_id, doc_id):
    """
    Function to store reserved document information in the database.
    """
    try:
        # Connect to the database
        db = DB()

        # SQL query to insert reserved document data into a new table
        query = f"""
        INSERT INTO RESERVED_DOCUMENTS (RID, DOCID)
        VALUES ('{reader_id}', '{doc_id}');
        """
        
        # Execute the SQL query
        result = db.query(query)

        # Check if the query was successful
        if result.status:
            print("Reserved document information stored successfully.")
        else:
            print("Error storing reserved document information.")

    except Exception as e:
        print("An error occurred:", e)

    finally:
        try:
            # Close the database connection
            db.close()
        except Exception as ce:
            print("An error occurred while closing the cursor:", ce)

# Create a new table for storing reserved documents if it doesn't exist
def create_reserved_documents_table():
    try:
        db = DB()

        # SQL query to create a new table for storing reserved documents
        query = """
        CREATE TABLE IF NOT EXISTS RESERVED_DOCUMENTS (
            RID VARCHAR(50),
            DOCID VARCHAR(50),
            RESERVED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (RID, DOCID),
            FOREIGN KEY (RID) REFERENCES READER(RID),
            FOREIGN KEY (DOCID) REFERENCES DOCUMENT(DOCID)
        );
        """
        
        
        # Execute the SQL query
        result = db.query(query)

        # Check if the query was successful
        if result.status:
            print("Reserved documents table created successfully.")
        else:
            print("Error creating reserved documents table.")

    except Exception as e:
        print("An error occurred:", e)

    finally:
        try:
            # Close the database connection
            db.close()
        except Exception as ce:
            print("An error occurred while closing the cursor:", ce)

if __name__ == "__main__":
    # Create the reserved documents table
    create_reserved_documents_table()

    # Example usage: take user input for reader ID and document ID
    reader_id = input("Enter the reader ID: ")
    doc_id = input("Enter the document ID: ")

    # Call the function to store reserved document information
    store_reserved_document(reader_id, doc_id)
