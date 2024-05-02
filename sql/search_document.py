import json
from datetime import date
from sql.db import DB

class DBResponse:
    def __init__(self, status, row=None, rows=None):
        self.status = status
        if row is not None:
            self.row = row
        else:
            self.row = None  # return none
        if rows is not None:
            self.rows = rows
        else:
            self.rows = []  # return empty list

    def __str__(self):
        # Convert date objects to strings before serialization
        formatted_row = {k: v.isoformat() if isinstance(v, date) else v for k, v in self.row.items()} if self.row else None
        formatted_rows = [{k: v.isoformat() if isinstance(v, date) else v for k, v in row.items()} for row in self.rows] if self.rows else None
        return json.dumps({"status": self.status, "row": formatted_row, "rows": formatted_rows})

class SearchDocumentCopy:
    """
    Used to search for a document copy in the database
    """

    @staticmethod
    def search_document_copy(document_id: str, copy_id: str, bid: str) -> dict:
        """
        Used to search for a document copy in the database

        Args:
          document_id (str): The document copy ID to search for
          copy_id (str): The copy ID to search for
          bid (str): The branch ID to search for

        Returns:
          dict: A dictionary containing the metadata of the document copy
        """

        # SQL query to check the existence of the document copy
        check_copy_existence_query = f"""
        SELECT COUNT(*)
        FROM COPY COP
        WHERE COP.DOCID = '{document_id}' AND COP.COPYNO = '{copy_id}' AND COP.BID = '{bid}';
        """

        # Execute the SQL query using the DB class
        copy_exists = DB.selectAll(check_copy_existence_query)

        # Check if the query was successful and the document copy exists
        if copy_exists and copy_exists.status:
            if copy_exists.row and copy_exists.row["COUNT(*)"] == 0:
                return {
                    "query_result": [],
                    "descriptive_error": "The document copy does not exist, either the document ID, copy ID, or branch ID is incorrect."
                }
        else:
            return {
                "query_result": [],
                "descriptive_error": "Error executing SQL query or no response received."
            }

        # SQL query to check if the copy is borrowed
        search_copy_query_in_borrows = f"""
        SELECT COUNT(*)
        FROM BORROWS BOR
        WHERE BOR.DOCID = '{document_id}' AND BOR.COPYNO = '{copy_id}' AND BOR.BID = '{bid}';
        """

        # Execute the SQL query using the DB class
        copy_borrowed = DB.selectAll(search_copy_query_in_borrows)

        # SQL query to check if the copy is reserved
        search_copy_query_in_reserves = f"""
        SELECT COUNT(*)
        FROM RESERVES RES
        WHERE RES.DOCID = '{document_id}' AND RES.COPYNO = '{copy_id}' AND RES.BID = '{bid}';
        """

        # Execute the SQL query using the DB class
        copy_reserved = DB.selectAll(search_copy_query_in_reserves)

        # Check if the copy is borrowed
        if copy_borrowed and copy_borrowed.status:
            if copy_borrowed.row and copy_borrowed.row["COUNT(*)"] >= 1:
                # SQL query to search for the borrowed copy details
                search_query = f"""
                SELECT BOR.*, BORW.BDTIME, BORW.RDTIME
                FROM BORROWS BOR, BORROWING BORW
                WHERE BOR.DOCID = '{document_id}' AND BOR.COPYNO = '{copy_id}' AND BOR.BID = '{bid}' AND BOR.BOR_NO = BORW.BOR_NO;
                """
                return DB.selectAll(search_query)

        # Check if the copy is reserved
        elif copy_reserved and copy_reserved.status:
            if copy_reserved.row and copy_reserved.row["COUNT(*)"] >= 1:
                # SQL query to search for the reserved copy details
                search_query = f"""
                SELECT RES.*, RESV.DTIME
                FROM RESERVES RES, RESERVATION RESV
                WHERE RES.DOCID = '{document_id}' AND RES.COPYNO = '{copy_id}' AND RES.BID = '{bid}' AND RES.RESERVATION_NO = RESV.RES_NO;
                """
                return DB.selectAll(search_query)

        # If not borrowed or reserved, return copy details
        search_query = f"""
        SELECT *
        FROM COPY
        WHERE DOCID = '{document_id}' AND COPYNO = '{copy_id}' AND BID = '{bid}';
        """
        return DB.selectAll(search_query)

# Example usage:
if __name__ == "__main__":
    # Take user input for document ID, copy ID, and branch ID
    document_id = input("Enter the document ID: ")
    copy_id = input("Enter the copy ID: ")
    bid = input("Enter the branch ID: ")

    # Call the function with user input
    result = SearchDocumentCopy.search_document_copy(document_id, copy_id, bid)

    if result:
        print("Document copy information:", result)
    else:
        print("No document copy found")
