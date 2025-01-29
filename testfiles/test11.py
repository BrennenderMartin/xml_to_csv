import os
import xml.etree.ElementTree as ET
import pandas as pd

def get_item(path, root):
    """
    Extracts the value from the XML path. Supports both single paths (string)
    and multiple paths (list).
    """
    if isinstance(path, str):
        element = root.find(path)
        if element is not None and element.text:
            return element.text.strip()
    elif isinstance(path, list):
        return " ".join(
            root.find(p).text.strip() if root.find(p) is not None and root.find(p).text else ""
            for p in path
        )
    return ""

def create_csv(mapping, file_name, root, data):
    """
    Creates a DataFrame from the mapping and appends the data to the CSV.
    """
    row = {}
    for key, value in mapping.items():
        entry = get_item(value, root)
        row[key] = entry

    # Append the row to the data list
    data.append(row)

    # Save to CSV
    df = pd.DataFrame(data, dtype=object)
    df.to_csv(file_name, sep=";", index=False, quoting=3)

mapping_SUNTR ={"pickup_time": "transfers/transfer/origin/pickup_time",
                "pickup_address": "transfers/transfer/origin/name",
                "pickup_address_complete": "",
                "pickup_latitude": "",
                "pickup_longitude": "",
                "dropoff_address": "transfers/transfer/destination/accommodation/address",
                "dropoff_address_complete": "",
                "dropoff_latitude": "",
                "dropoff_longitude": "",
                "via_address": "",
                "via_address_complete": "",
                "vehicle_type_name": "transfers/transfer/vehicle/title",
                "estimated_distance": "",
                "estimated_duration": "",
                "ref_number": "reference",
                "total_price": "transfers/transfer/transfer_rate",
                "discount_price": "",
                "discount_code": "",
                "service_name": "",
                "service_duration_in_hours": "",
                "passenger1_name": ["lead_passenger/name", "lead_passenger/surname"],
                "passenger1_email": "lead_passenger/email",
                "passenger1_phone": "lead_passenger/mobile",
                "passenger2_name": "",
                "passenger2_email": "",
                "passenger2_phone": "",
                "requirements": "",
                "passenger_count": "transfers/transfer/passengers/total_passengers",
                "luggage_count": "",
                "hand_luggage_count": "",
                "child_seat_count": "transfers/transfer/passengers/number_children",
                "booster_seat_count": "",
                "infant_seat_count": "transfers/transfer/passengers/number_babies",
                "wheelchair_count": "",
                "pickup_flight_number": "transfers/transfer/origin/flight/flight_number",
                "pickup_flight_time": "",
                "pickup_flight_city": "",
                "dropoff_flight_number": "",
                "dropoff_flight_time": "",
                "dropoff_flight_city": "",
                "meet_and_greet": "",
                "meeting_point": "",
                "meeting_board": "",
                "waiting_time_in_minutes": "",
                "source_name": "",
                "source_details": "",
                "custom_field_1": "",
                "custom_field_2": "",
                "custom_field_3": "",
                "custom_field_4": "",
                "admin_note": "",
                "ip_address": "",
                "created_date": "transfers/transfer/creation_date"
}

mapping2 = {"pickup_time": "pickupDate",
            "pickup_address": "originDetails/name",
            "pickup_address_complete": "",
            "pickup_latitude": "",
            "pickup_longitude": "",
            "dropoff_address": "destinationDetails/name",
            "dropoff_address_complete": "",
            "dropoff_latitude": "",
            "dropoff_longitude": "",
            "via_address": "",
            "via_address_complete": "",
            "vehicle_type_name": "transportDetails/vehicleType",
            "estimated_distance": "",
            "estimated_duration": "",
            "ref_number": "",
            "total_price": "price",
            "discount_price": "",
            "discount_code": "",
            "service_name": "",
            "service_duration_in_hours": "",
            "passenger1_name": "passengerInformation/name",
            "passenger1_email": "",
            "passenger1_phone": "passengerInformation/phone",
            "passenger2_name": "",
            "passenger2_email": "",
            "passenger2_phone": "",
            "requirements": "",
            "passenger_count": "transportDetails/adults",
            "luggage_count": "transportDetails/includedLuggage",
            "hand_luggage_count": "",
            "child_seat_count": "transportDetails/childs",
            "booster_seat_count": "",
            "infant_seat_count": "transportDetails/infants",
            "wheelchair_count": "",
            "pickup_flight_number": "originDetails/transportNumber",
            "pickup_flight_time": "",
            "pickup_flight_city": "",
            "dropoff_flight_number": "",
            "dropoff_flight_time": "",
            "dropoff_flight_city": "",
            "meet_and_greet": "",
            "meeting_point": "",
            "meeting_board": "",
            "waiting_time_in_minutes": "",
            "source_name": "",
            "source_details": "",
            "custom_field_1": "",
            "custom_field_2": "",
            "custom_field_3": "",
            "custom_field_4": "",
            "admin_note": "",
            "ip_address": "",
            "created_date": ""
}


# Specify the folder containing XML files
folder_path = "xml_to_csv/input"  # Replace with your folder path

# Initialize the shared dataset
data = []

# Iterate over all files in the folder
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)

    # Check if it's an XML file
    if not file_name.endswith(".xml"):
        print(f"Skipping non-XML file: {file_name}")
        continue

    print(f"\nProcessing file: {file_name}")

    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Determine the mapping based on the reference
    reference = root.find("reference")
    if reference is not None and "SUNTR" in reference.text:
        print(f"The reference contains SUNTR in {file_name}.")
        chosen_mapping = mapping_SUNTR
    else:
        print(f"The reference does not contain SUNTR in {file_name}. Found: {reference.text if reference is not None else 'None'}")
        chosen_mapping = mapping2

    # Extract data and append it as a new row
    create_csv(chosen_mapping, "xml_to_csv/output/output.csv", root, data)
