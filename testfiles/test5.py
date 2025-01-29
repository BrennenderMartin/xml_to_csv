import xml.etree.ElementTree as ET
import csv

# Define mappings between XML tags and CSV column names
tag_to_csv_mapping = {
    "reference": "Booking Reference",
    "agency_name": "Agency Name",
    "customer_name": "Customer Name",
    "customer_surname": "Customer Surname",
    "passenger_name": "Lead Passenger Name",
    "passenger_surname": "Lead Passenger Surname",
    "vehicle_title": "Vehicle Title",
    "pickup_location": "Pickup Location",
    "dropoff_location": "Dropoff Location",
    "transfer_rate": "Transfer Rate"
}

def extract_booking_info_to_csv(xml_file, csv_template, output_csv):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extract relevant information from the XML
    booking_data = {
        "reference": root.findtext("reference"),
        "agency_name": root.findtext("agency_name"),
        "customer_name": root.find("customer/name").text if root.find("customer/name") is not None else None,
        "customer_surname": root.find("customer/surname").text if root.find("customer/surname") is not None else None,
        "passenger_name": root.find("lead_passenger/name").text if root.find("lead_passenger/name") is not None else None,
        "passenger_surname": root.find("lead_passenger/surname").text if root.find("lead_passenger/surname") is not None else None,
        "vehicle_title": root.find("transfers/transfer/vehicle/title").text if root.find("transfers/transfer/vehicle/title") is not None else None,
        "pickup_location": root.find("transfers/transfer/origin/name").text if root.find("transfers/transfer/origin/name") is not None else None,
        "dropoff_location": root.find("transfers/transfer/destination/name").text if root.find("transfers/transfer/destination/name") is not None else None,
        "transfer_rate": root.find("transfers/transfer/transfer_rate").text if root.find("transfers/transfer/transfer_rate") is not None else None,
    }

    # Read the CSV template to get column names
    with open(csv_template, mode="r", encoding="utf-8") as template_file:
        reader = csv.DictReader(template_file)
        fieldnames = reader.fieldnames

    # Write extracted data to the output CSV
    with open(output_csv, mode="w", newline="\n", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()

        # Prepare a row matching the template fields
        row = {col: booking_data.get(tag, "") for tag, col in tag_to_csv_mapping.items() if col in fieldnames}
        print(row)
        writer.writerow(row)

    print(f"Booking information successfully written to '{output_csv}'")

# File paths
xml_file = 'Python/Praktikum/booking_4092840.xml'  # XML file path
csv_template = 'Python/Praktikum/ETO Bookings import template.csv'  # CSV template path
output_csv = 'merged_booking_data.csv'  # Output CSV file

# Run the merging process
extract_booking_info_to_csv(xml_file, csv_template, output_csv)
