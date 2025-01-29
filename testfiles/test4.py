import xml.etree.ElementTree as ET
import csv

# Define a mapping of XML tags to CSV column names
tag_to_csv_mapping = {
    "Title": "Book Title",
    "Author": "Creator",
    "Year": "Publication Year",
    "Genre": "Category"
}

def extract_first_book_to_csv(xml_file, csv_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Find the first book
    first_book = root.find('Book')
    if first_book is None:
        print("No books found in the XML file.")
        return

    # Extract book information based on the mapping
    book_data = {}
    for xml_tag, csv_column in tag_to_csv_mapping.items():
        element = first_book.find(xml_tag)
        if element is not None:
            book_data[csv_column] = element.text
        else:
            book_data[csv_column] = None  # Handle missing fields gracefully

    # Write the book data to a CSV file
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=tag_to_csv_mapping.values())
        writer.writeheader()
        writer.writerow(book_data)

    print(f"First book information written to {csv_file}")

# File paths
xml_file = 'Python/Praktikum/file.xml'  # Path to the uploaded XML file
csv_file = 'first_book.csv'      # Output CSV file

# Run the extraction
extract_first_book_to_csv(xml_file, csv_file)
