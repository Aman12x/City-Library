from sql.db import DB
from datetime import datetime

def run_sql_query(start_datetime_str, end_datetime_str):
    """
    Function to run SQL query using the DB.query() method.
    """
    try:
        # Connect to the database
        db = DB()

        query = f"""
        SELECT BRAN.BID, BRAN.BNAME, SUM(GREATEST(DATEDIFF(BORW.RDTIME, BORW.BDTIME) - 20, 0) * 0.2) / COUNT(*) AS TOTAL_FINE_COLLECTED
        FROM BRANCH AS BRAN, BORROWS AS BOR, BORROWING AS BORW
        WHERE BRAN.BID = BOR.BID AND BOR.BOR_NO = BORW.BOR_NO AND BORW.BDTIME >= '{start_datetime_str}' AND BORW.RDTIME <= '{end_datetime_str}'
        GROUP BY BRAN.BID
        ORDER BY SUM(GREATEST(DATEDIFF(BORW.RDTIME, BORW.BDTIME) - 20, 0)) / COUNT(*) DESC;
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
            print("An error occurred while closing the connection:", ce)

if __name__ == "__main__":
    # Get user input for start and end dates
    start_date_input = input("Enter the start date (YYYY-MM-DD): ")
    end_date_input = input("Enter the end date (YYYY-MM-DD): ")

    try:
        # Convert user input to datetime objects
        start_datetime = datetime.strptime(start_date_input, '%Y-%m-%d')
        end_datetime = datetime.strptime(end_date_input, '%Y-%m-%d')

        # Format datetime objects to string
        start_datetime_str = start_datetime.strftime('%Y-%m-%d %H:%M:%S')
        end_datetime_str = end_datetime.strftime('%Y-%m-%d %H:%M:%S')

        # Call the function to run the SQL query
        run_sql_query(start_datetime_str, end_datetime_str)

    except ValueError:
        print("Invalid date format. Please enter dates in the format YYYY-MM-DD.")
