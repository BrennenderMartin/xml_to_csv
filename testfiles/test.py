import xml.etree.ElementTree as ET

#list of all the items, that are in the csv-file
titleList= ["pickup_time",
            "pickup_address",
            "pickup_address_complete",
            "pickup_latitude",
            "pickup_longitude",
            "dropoff_address",
            "dropoff_address_complete",
            "dropoff_latitude",
            "dropoff_longitude",
            "via_address",
            "via_address_complete",
            "vehicle_type_name",
            "estimated_distance",
            "estimated_duration",
            "ref_number",
            "total_price",
            "discount_price",
            "discount_code",
            "service_name",
            "service_duration_in_hours",
            "passenger1_name",
            "passenger1_email",
            "passenger1_phone",
            "passenger2_name",
            "passenger2_email",
            "passenger2_phone",
            "requirements",
            "passenger_count",
            "luggage_count",
            "hand_luggage_count",
            "child_seat_count",
            "booster_seat_count",
            "infant_seat_count",
            "wheelchair_count",
            "pickup_flight_number",
            "pickup_flight_time",
            "pickup_flight_city",
            "dropoff_flight_number",
            "dropoff_flight_time",
            "dropoff_flight_city",
            "meet_and_greet",
            "meeting_point",
            "meeting_board",
            "waiting_time_in_minutes",
            "source_name",
            "source_details",
            "custom_field_1",
            "custom_field_2",
            "custom_field_3",
            "custom_field_4",
            "admin_note",
            "ip_address",
            "created_date"]

testList = ["Title",
            "Author",
            "Month",
            "Year"]

csv_list = []

path = 'Python/Praktikum/file.xml'

def get_mag(file_path, magazine_id):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    for magazine in root.findall("Magazine"):
        if magazine.get("id") == magazine_id:
            
            title = magazine.find('Title').text
            author = magazine.find('Issue').text
            month = magazine.find('Month').text
            year = magazine.find('Year').text
            
            return {
                "Title": title,
                "Author": author,
                "Month": month,
                "Year": year
            }


def get_book_info_by_id(file_path, book_id):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    
    # Find the book with the matching id
    for book in root.findall('Book'):
        if book.get('id') == book_id:
            """
            matrix = []
            for i, value in enumerate(testList):
                matrix.append([testList[i], value])
            return matrix
            """
            # Extract book information
            title = book.find('Title').text
            author = book.find('Author').text
            year = book.find('Year').text
            genre = book.find('Genre').text

            # Return the extracted information
            return {
                "Title": title,
                "Author": author,
                "Year": year,
                "Genre": genre
            }
            
            
    return None

"""
if __name__ == "__main__":
    file_path = path
    mag_id = input("Enter the magazine ID: ").strip()
    
    mag_info = get_mag(file_path, mag_id)
    print(mag_info)
    
    if mag_info:
        print("Magazine Information:")
        for key, value in mag_info.items():
            print(f"{key}: {value}")
            csv_list.append([key, value])
    else:
        print(f"No magazine found with ID {mag_id}.")
    """

#print(csv_list)

""""""
# Example Usage
if __name__ == "__main__":
    file_path = path  # Path to your XML file
    book_id = input("Enter the book ID: ").strip()

    # Fetch book information
    book_info = get_book_info_by_id(file_path, book_id)

    if book_info:
        print("Book Information:")
        for key, value in book_info.items():
            print(f"{key}: {value}")
    else:
        print(f"No book found with ID {book_id}.")
