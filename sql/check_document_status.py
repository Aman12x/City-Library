from sql.db import DB

def check_document_status(doc_id, copy_no):
    # Initialize status variable
    status = "Neither"

    # Check if the document exists in the DOCUMENT table
    sql_query = f"""
        SELECT DOCID
        FROM DOCUMENT
        WHERE DOCID = {doc_id};
    """
    response = DB.selectAll(sql_query)
    if not response.status or not response.rows:
        return "Document does not exist"

    # Check if the document is borrowed
    sql_query = f"""
        SELECT BID
        FROM BORROWS
        WHERE DOCID = {doc_id} AND COPYNO = {copy_no};
    """
    response = DB.selectAll(sql_query)
    if response.status and response.rows:
        status = "Borrowed"
        return status

    # Check if the document is reserved
    sql_query = f"""
        SELECT RESERVATION_NO
        FROM RESERVES
        WHERE DOCID = {doc_id} AND COPYNO = {copy_no};
    """
    response = DB.selectAll(sql_query)
    if response.status and response.rows:
        status = "Reserved"
        return status

    return status

# Example usage
doc_id = int(input("Enter the document ID: "))
copy_no = int(input("Enter the copy number: "))

status = check_document_status(doc_id, copy_no)
if status == "Borrowed":
    print("The document is borrowed.")
elif status == "Reserved":
    print("The document is reserved.")
elif status == "Document does not exist":
    print("The document does not exist.")
else:
    print("The document is neither borrowed nor reserved.")
