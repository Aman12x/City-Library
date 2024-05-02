from sql.db import DB
import random
import string

def checkout_document(reader_id, borrow_number, doc_id, bid, copy_no):
    """
    Function to checkout a document by a reader with a specified borrow number, document ID, branch ID, and copy number.
    """
    try:
        # Connect to the database
        db = DB()

        # Check if the document is already borrowed
        doc_borrowed_query = f"""
        SELECT COUNT(*)
        FROM BORROWS
        WHERE DOCID = '{doc_id}';
        """
        doc_borrowed_result = db.selectOne(doc_borrowed_query)

        if doc_borrowed_result.status and doc_borrowed_result.row['COUNT(*)'] > 0:
            print("The document is already borrowed.")
            return

        # Check if the copy exists at the specified branch
        copy_branch_query = f"""
        SELECT COUNT(*)
        FROM COPY
        WHERE DOCID = '{doc_id}' AND BID = '{bid}' AND COPYNO = '{copy_no}';
        """
        copy_branch_result = db.selectOne(copy_branch_query)

        if not (copy_branch_result.status and copy_branch_result.row['COUNT(*)'] > 0):
            print("The specified copy is not available at the provided branch.")
            return

        # Insert the document into the BORROWS table
        insert_borrow_query = f"""
        INSERT INTO BORROWS (BOR_NO, DOCID, COPYNO, BID, RID)
        VALUES ('{borrow_number}', '{doc_id}', '{copy_no}', '{bid}', '{reader_id}');
        """
        insert_result = db.query(insert_borrow_query)

        # Check if the insertion was successful
        if insert_result.status:
            print("Document successfully checked out.")
        else:
            print("Error checking out the document.")

    except Exception as e:
        print("An error occurred:", e)

    finally:
        try:
            # Close the database connection
            db.close()
        except Exception as ce:
            print("An error occurred while closing the cursor:", ce)

if __name__ == "__main__":
    # Example usage: take user input for reader ID, borrow number, document ID, branch ID, and copy number
    reader_id = input("Enter the reader ID: ")
    borrow_number = input("Enter the borrow number: ")
    doc_id = input("Enter the document ID: ")
    bid = input("Enter the Branch ID: ")
    copy_no = input("Enter the Copy Number: ")

    # Call the function to checkout the document with the specified borrow number, document ID, branch ID, and copy number
    checkout_document(reader_id, borrow_number, doc_id, bid, copy_no)
