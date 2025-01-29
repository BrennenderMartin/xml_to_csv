import xml.etree.ElementTree as ET
import pandas as pd

def parse_element(element, level=0, parent_tag=None):
    """
    Recursively parse an XML element, print its tag, attributes, and text,
    and store it in a list with context (parent tag).
    """
    indent = "  " * level
    
    if element.text and element.text.strip():
        data_list.append({
            "parent": parent_tag,
            "tag": element.tag,
            "text": element.text.strip(),
            "attributes": element.attrib
        })

    for child in element:
        parse_element(child, level + 1, parent_tag=element.tag)

def get_item(path):
    if isinstance(path, str):
        # Single path case
        element = root.find(path)
        if element is not None and element.text:
            return element.text.strip()
    elif isinstance(path, list):
        # Concatenate values from multiple paths
        return " ".join(
            root.find(p).text.strip() if root.find(p) is not None and root.find(p).text else ""
            for p in path
        )
    return ""

def create_csv(mapping):
    parse_element(root)
    
    data = []
    
    row = {}
    for key, value in mapping.items():
        entry = get_item(value)
        row[key] = entry
    
    data.append(row)  # Append the row to the data list
    df = pd.DataFrame(data, dtype=object)
    
    #df.to_csv("test5.csv", sep=";", index=False, quoting=3)
    print(df.T)

# with the mapping I have:
# the csv as key and
# the xml as value
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

path = 'xml_to_csv/booking_4095060.xml'
path2 = 'xml_to_csv/1754335.xml'

# Load and parse the XML file
tree = ET.parse(path2)
root = tree.getroot()

reference = root.find("reference")

data_list = []

def main():
    chosen_mapping = ""
    # Check if the reference matches
    if reference is not None and reference.text == "SUNTR_QX5060":
        print("The reference is SUNTR_QX5060.")
        chosen_mapping = mapping_SUNTR
    else:
        print(f"The reference is not SUNTR_QX5060. Found:{reference.text if reference is not None else 'None'}")
        chosen_mapping = mapping2
    
    create_csv(chosen_mapping)

main()