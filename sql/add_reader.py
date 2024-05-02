from enum import Enum
from mysql.connector import Error
import json
from sql.db import DB

class CRUD(Enum):
    CREATE = 1,
    READ = 2,
    UPDATE = 3,
    DELETE = 4, 
    ALTER = 5


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
        return json.dumps(self.__dict__)

class AddReader:
    """
    Used to add a reader to the database
    """

    @staticmethod
    def add_reader(reader_id: str, reader_type: str, reader_name: str, reader_address: str, reader_phone: str) -> dict:
        """
        Used to add a reader to the database

        Args:
          reader_id (str): The ID of the reader to add
          reader_type (str): The type of the reader
          reader_name (str): The name of the reader
          reader_address (str): The address of the reader
          reader_phone (str): The phone number of the reader

        Returns:
          dict: A dictionary containing the result of the operation
        """

        # Check if the reader already exists
        check_if_reader_exists_query = f"""
        SELECT COUNT(*)
        FROM READER
        WHERE RID = '{reader_id}';
        """ 
        reader_exists_result = DB.selectAll(check_if_reader_exists_query)
        if reader_exists_result.status:
            if reader_exists_result.rows[0]["COUNT(*)"] != 0:
                return {
                    "status": False,
                    "message": "Reader already exists with the provided ID."
                }

        # Add the reader to the database
        add_reader_query = f"""
        INSERT INTO READER (RID, RTYPE, RNAME, RADDRESS, PHONE_NO) 
        VALUES ('{reader_id}', '{reader_type}', '{reader_name}', '{reader_address}', '{reader_phone}');
        """
        add_reader_result = DB.query(add_reader_query)

        # Check if the insertion was successful
        if add_reader_result.status:
            return {
                "status": True,
                "message": "Reader added successfully.",
                "new_reader_details": {
                    "RID": reader_id,
                    "RTYPE": reader_type,
                    "RNAME": reader_name,
                    "RADDRESS": reader_address,
                    "PHONE_NO": reader_phone
                }
            }
        else:
            return {
                "status": False,
                "message": "Failed to add reader to the database."
            }

# Example usage:
if __name__ == "__main__":
    # Take user input for reader details
    reader_id = input("Enter the reader ID: ")
    reader_type = input("Enter the reader type: ")
    reader_name = input("Enter the reader name: ")
    reader_address = input("Enter the reader address: ")
    reader_phone = input("Enter the reader phone number: ")

    # Call the function with user input
    result = AddReader.add_reader(reader_id, reader_type, reader_name, reader_address, reader_phone)

    # Print the result
    print(result)
