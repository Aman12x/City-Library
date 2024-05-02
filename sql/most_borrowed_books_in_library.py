from sql.db import DB  

def find_most_borrowed_book(library_name, limit=1):
    """
    Function to find the most borrowed book in a specific library.
    """
    try:
        db = DB()
        query = f"""
        SELECT BID, COUNT(DISTINCT BO.DOCID)
        FROM BORROWS AS BOR, BOOK AS BO
        WHERE BOR.DOCID = BO.DOCID AND BOR.BID IN (
            SELECT DISTINCT BID
            FROM BRANCH
            WHERE BNAME='{library_name}'
        )
        GROUP BY BID
        ORDER BY COUNT(DISTINCT BO.DOCID) DESC
        LIMIT {limit};
        """
        result = db.selectAll(query)

        # Print the result
        if result.status:
            if result.rows:
                print(f"The most borrowed book in library '{library_name}' is:")
                for row in result.rows:
                    print("BID:", row['BID'])
                    print("Borrow Count:", row['COUNT(DISTINCT BO.DOCID)'])
            else:
                print(f"No books found in library '{library_name}'.")
        else:
            print("Error executing the query.")

    except Exception as e:
        print("An error occurred:", e)

    finally:
        try:
            # Close the database connection
            db.close()
        except Exception as ce:
            print("An error occurred while closing the cursor:", ce)

if __name__ == "__main__":
    # Get the library name from user input
    library_name = input("Enter the library name: ")

    # Call the function to find the most borrowed book in the library
    find_most_borrowed_book(library_name)
