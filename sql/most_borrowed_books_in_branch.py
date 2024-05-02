from sql.db import DB

def get_most_borrowed_books(branch_no, limit):
    try:
        # Connect to the database
        db = DB()

        # SQL query to get the N most borrowed books in a specific branch
        query = f"""
        SELECT BO.DOCID, COUNT(DISTINCT BOR.RID) AS num_borrowers
        FROM BORROWS AS BOR
        INNER JOIN BOOK AS BO ON BOR.DOCID = BO.DOCID
        WHERE BOR.BID='{branch_no}'
        GROUP BY BO.DOCID
        ORDER BY num_borrowers DESC
        LIMIT {limit};
        """

        # Execute the SQL query
        result = db.selectAll(query)

        # Check if the query was successful
        if result.status:
            if result.rows:
                print("Most borrowed books in branch", branch_no, ":")
                for row in result.rows:
                    print(f"Book DOCID: {row['DOCID']}, Number of Borrowers: {row['num_borrowers']}")
            else:
                print("No books found for the specified branch.")
        else:
            print("Error executing the query.")

    except Exception as e:
        print("An error occurred:", e)

    finally:
        try:
            # Close the database connection
            db.close()
        except Exception as ce:
            print("An error occurred while closing the connection:", ce)

if __name__ == "__main__":
    # Get user input for branch number and limit
    branch_no = input("Enter the branch number: ")
    limit = int(input("Enter the limit: "))

    # Call the function to get the most borrowed books
    get_most_borrowed_books(branch_no, limit)
