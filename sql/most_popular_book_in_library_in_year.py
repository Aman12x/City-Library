from sql.db import DB

def most_popular_books(branch_name, year, limit):
    try:
        # Connect to the database
        db = DB()

        # SQL query to retrieve the most popular books in a year at a specific branch
        sql_query = f"""
            SELECT BO.DOCID, DOC.TITLE, COUNT(DISTINCT REA.RID) AS NO_OF_TIMES_BORROWED 
            FROM BORROWS AS BOR
            JOIN BOOK AS BO ON BO.DOCID = BOR.DOCID
            JOIN READER AS REA ON REA.RID = BOR.RID
            JOIN BORROWING AS BORW ON BORW.BOR_NO = BOR.BOR_NO
            JOIN DOCUMENT AS DOC ON DOC.DOCID = BO.DOCID
            WHERE YEAR(BORW.BDTIME) = {year} 
                AND BOR.BID = (SELECT BID FROM BRANCH WHERE BNAME = '{branch_name}')
                AND BO.DOCID IN (
                    SELECT DOCID
                    FROM BOOK
                )
            GROUP BY BO.DOCID
            ORDER BY COUNT(DISTINCT REA.RID) DESC
            LIMIT {limit};
        """

        # Execute the SQL query
        result = db.selectAll(sql_query)

        # Check if the query was successful
        if result.status:
            return result.rows
        else:
            print("Error executing SQL query")
            return None

    except Exception as e:
        print("An error occurred:", e)
        return None

if __name__ == "__main__":
    # Take user input for branch name, year, and limit
    branch_name = input("Enter the name of the branch: ")
    year = input("Enter the year (YYYY) to retrieve most popular books: ")
    limit = int(input("Enter the limit for the number of results: "))

    # Call the function with user input
    result = most_popular_books(branch_name, year, limit)

    if result:
        print(f"Most popular books in {branch_name} branch for the year {year}:")
        for i, book in enumerate(result, 1):
            print(f"{i}. Title: {book['TITLE']}, DocID: {book['DOCID']}, No. of Times Borrowed: {book['NO_OF_TIMES_BORROWED']}")
    else:
        print("No data found for the given input")
