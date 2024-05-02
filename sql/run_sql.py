# main.py
from sql.db import DB
from add_document_copy import AddDocument
from add_reader import AddReader

def main():
    print("1. Add Document")
    print("2. Add Reader")
    choice = input("Enter your choice: ")

    if choice == "1":
        document_id = input("Enter the document ID: ")
        title = input("Enter the title of the document: ")
        publication_date = input("Enter the publication date of the document (YYYY-MM-DD): ")
        publisher_id = int(input("Enter the publisher ID of the document: "))

        result = AddDocument.add_document(document_id, title, publication_date, publisher_id)
        print(result)

    elif choice == "2":
        reader_id = input("Enter the reader ID: ")
        reader_type = input("Enter the reader type: ")
        reader_name = input("Enter the reader name: ")
        reader_address = input("Enter the reader address: ")
        reader_phone = input("Enter the reader phone number: ")

        result = AddReader.add_reader(reader_id, reader_type, reader_name, reader_address, reader_phone)
        print(result)

    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
