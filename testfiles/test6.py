import xml.etree.ElementTree as ET
import pandas as pd

# Parse the XML file
file_path = 'Python/Praktikum/file.xml'  # Path to your XML file
tree = ET.parse(file_path)
root = tree.getroot()

# Initialize lists for books and magazines
books_data = []
magazines_data = []

# Extract book data
for book in root.findall('Book'):
    book_data = {
        "ID": book.get("id"),
        "Title": book.findtext("Title"),
        "Author": book.findtext("Author"),
        "Year": book.findtext("Year"),
        "Genre": book.findtext("Genre"),
        "Type": "Book"
    }
    books_data.append(book_data)

# Extract magazine data
for magazine in root.findall('Magazine'):
    magazine_data = {
        "ID": magazine.get("id"),
        "Title": magazine.findtext("Title"),
        "Issue": magazine.findtext("Issue"),
        "Month": magazine.findtext("Month"),
        "Year": magazine.findtext("Year"),
        "Type": "Magazine"
    }
    magazines_data.append(magazine_data)

# Combine books and magazines into a single list
all_data = books_data + magazines_data

# Create a DataFrame
df = pd.DataFrame(all_data)

# Display the DataFrame
print(df)
