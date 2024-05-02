from sql.db import DB

class AddDocument:
    """
    Used to add a document to the database
    """

    @staticmethod
    def add_document(document_id: str, title: str, publication_date: str, publisher_id: int) -> dict:
        """
        Used to add a document to the database

        Args:
            document_id (str): The ID of the document
            title (str): The title of the document
            publication_date (str): The publication date of the document in the format 'YYYY-MM-DD'
            publisher_id (int): The ID of the publisher of the document

        Returns:
            dict: A dictionary containing the result of the operation
        """

        # Add the document to the database
        add_document_query = f"""
        INSERT INTO DOCUMENT (DOCID, TITLE, PDATE, PUBLISHERID) 
        VALUES ('{document_id}', '{title}', '{publication_date}', {publisher_id});
        """
        add_document_result = DB.query(add_document_query)

        # Check if the insertion was successful
        if add_document_result.status:
            return {
                "status": True,
                "message": "Document added successfully.",
                "new_document_details": {
                    "DOCID": document_id,
                    "TITLE": title,
                    "PDATE": publication_date,
                    "PUBLISHERID": publisher_id
                }
            }
        else:
            return {
                "status": False,
                "message": "Failed to add document to the database."
            }

# Example usage:
if __name__ == "__main__":
    # Take user input for document details
    document_id = input("Enter the document ID: ")
    title = input("Enter the title of the document: ")
    publication_date = input("Enter the publication date of the document (YYYY-MM-DD): ")
    publisher_id = int(input("Enter the publisher ID of the document: "))

    # Call the function with user input
    result = AddDocument.add_document(document_id, title, publication_date, publisher_id)

    # Print the result
    print(result)
