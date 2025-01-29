import os
import shutil
from datetime import datetime
import xml.etree.ElementTree as ET
import pandas as pd

"""Global variables:"""
sixSeater = "6 Seater"
sixSeaterPossibilities = ["Private Minivan", "Private Minivan (1-6)", "minivan"]

saloon = "Saloon"
saloonPossibilities = ["Private Transfer"]

folder_path = "xml_to_csv/input"  # Replace with your input folder path
output_folder =  "xml_to_csv/output/" # Replace with your output folder path
processed_folder = "xml_to_csv/processed" # Replace with your processed folder path

date_format = "%Y-%m-%d_%H-%M-%S" #Here: Year-Month-Day_Hour-Minute-Second

mapping_SUNTR ={"pickup_time": "transfers/transfer/origin/pickup_time",
                "pickup_address": "",
                "pickup_address_complete": "",
                "pickup_latitude": "",
                "pickup_longitude": "",
                "dropoff_address": "",
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

mapping_default = { "pickup_time": "pickupDate",
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

def create_csv_SUNTR(mapping, file_name, root, data):
    """
    Creates a DataFrame from the mapping and appends data for all transfers to the CSV.
    """
    # Find all <transfer> elements under <transfers>
    transfers = root.find("transfers")
    if transfers is None:
        print("No transfers found in this booking.")
        return

    # Iterate over each transfer
    for transfer in transfers.findall("transfer"):
        row = {}
        for key, value in mapping.items():
            # Special handling for pickup and dropoff addresses
            if key == "pickup_address":
                origin = transfer.find("origin")
                if origin is not None and origin.attrib.get("type") == "airport":
                    row[key] = get_item("name", origin)
                    appendix_ref_number = "a"
                elif origin is not None and origin.attrib.get("type") == "city":
                    row[key] = get_item("accommodation/address", transfer.find("origin"))
                    appendix_ref_number = "b"
                else:
                    row[key] = ""
            
            elif key == "dropoff_address":
                destination = transfer.find("destination")
                if destination is not None and destination.attrib.get("type") == "airport":
                    row[key] = get_item("name", destination)
                elif destination is not None and destination.attrib.get("type") == "city":
                    row[key] = get_item("accommodation/address", transfer.find("destination"))
                else:
                    row[key] = ""
            
            else:
                # Default behavior for other keys
                if "transfers/transfer/" in value:  # Adjust paths to be relative to the <transfer>
                    entry = get_item(value.replace("transfers/transfer/", ""), transfer)
                else:
                    entry = get_item(value, root)

                # Adjust vehicle type name
                if key == "vehicle_type_name" and entry in sixSeaterPossibilities:
                    entry = sixSeater
                elif key == "vehicle_type_name" and entry in saloonPossibilities:
                    entry = saloon
                elif key == "ref_number":
                    entry += appendix_ref_number
                row[key] = entry

        # Append the row for this transfer
        data.append(row)

    # Save to CSV
    df = pd.DataFrame(data, dtype=object)
    df.to_csv(file_name, sep=";", index=False, quoting=3)

def create_csv_default(mapping, file_name, root, data):
    """
    Creates a DataFrame from the mapping and appends all data to the CSV.
    """
    # Iterate over each transfer
    row = {}
    for key, value in mapping.items():
        entry = get_item(value, root)

        # Adjust vehicle type name
        if key == "vehicle_type_name" and entry in sixSeaterPossibilities:
            entry = sixSeater
        elif key == "vehicle_type_name" and entry in saloonPossibilities:
            entry = saloon

        row[key] = entry

    # Append the row for this transfer
    data.append(row)

    # Save to CSV
    df = pd.DataFrame(data, dtype=object)
    df.to_csv(file_name, sep=";", index=False, quoting=3)

# Initialize the shared dataset
data = []

# Create the output folder with the current date
date = datetime.now().strftime(date_format)
final_folder = os.path.join(processed_folder, date)
os.makedirs(final_folder, exist_ok=True)

if not os.listdir(folder_path):
    print("There are no xml files to be processed")
else:    
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
            create_csv_SUNTR(mapping_SUNTR, f"{output_folder}/output_{date}.csv", root, data)
        else:
            print(f"The reference does not contain SUNTR in {file_name}. Found: {reference.text if reference is not None else 'None'}")
            create_csv_default(mapping_default, f"{output_folder}/output_{date}.csv", root, data)

        # Extract data and append it as a new row
        
        
        # Move the processed XML file to the date-named folder
        new_file_path = os.path.join(final_folder, file_name)
        shutil.move(file_path, new_file_path)
        print(f"Moved file to: {new_file_path}")
