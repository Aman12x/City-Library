from sql.db import DB  # Import the DB class from db.py

def run_sql_query(reader_id):
    """
    Function to run SQL query using the DB.selectAll() method.
    """
    try:
        # Connect to the database
        db = DB()

        # Execute the SQL query
        query = f"""
        SELECT 
            R.RID, 
            R.RNAME, 
            DOC.TITLE, 
            BO.BDTIME, 
            BO.RDTIME, 
            GREATEST(DATEDIFF(BO.RDTIME, BO.BDTIME) - 20, 0) AS ADDITIONAL_DAYS_BORROWED, 
            0.2 * GREATEST(DATEDIFF(BO.RDTIME, BO.BDTIME) - 20, 0) AS FINE_IMPOSED_IN_DOLLARS
        FROM 
            READER AS R, 
            BORROWS AS B, 
            BORROWING AS BO, 
            COPY AS COP, 
            DOCUMENT AS DOC
        WHERE 
            R.RID = {reader_id}
            AND R.RID = B.RID 
            AND B.BOR_NO = BO.BOR_NO 
            AND B.DOCID = COP.DOCID 
            AND B.COPYNO = COP.COPYNO 
            AND B.BID = COP.BID 
            AND COP.DOCID = DOC.DOCID ;
        """
        result = db.selectAll(query)

        # Print the result
        if result.status:
            if result.rows:
                print("Result:")
                for row in result.rows:
                    print(row)
            else:
                print("No rows returned.")
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
    # Get the RID from user input
    reader_id = input("Enter the RID: ")

    # Call the function to run the SQL query
    run_sql_query(reader_id)
