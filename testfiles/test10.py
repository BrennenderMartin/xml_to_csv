import os
import xml.etree.ElementTree as ET
import pandas as pd

def parse_element(element, level=0, parent_tag=None):
    """
    Recursively parse an XML element, print its tag, attributes, and text,
    and store it in a list with context (parent tag).
    """
    if element.text and element.text.strip():
        data_list.append({
            "parent": parent_tag,
            "tag": element.tag,
            "text": element.text.strip(),
            "attributes": element.attrib
        })

    for child in element:
        parse_element(child, parent_tag=element.tag)

def get_item(path):
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

def create_csv(mapping, file_name):
    """
    Creates a DataFrame from the mapping and appends the data to the CSV.
    """
    parse_element(root)
    
    row = {}
    for key, value in mapping.items():
        entry = get_item(value)
        row[key] = entry

    # Append the row to the data list
    data.append(row)

    # Save to CSV
    df = pd.DataFrame(data, dtype=object)
    df.to_csv(file_name, sep=";", index=False, quoting=3)

# Define mappings for the XML paths
mapping_SUNTR = {
    "pickup_time": "transfers/transfer/origin/pickup_time",
    "pickup_address": "transfers/transfer/origin/name",
    "ref_number": "reference",
    "total_price": "transfers/transfer/transfer_rate",
    "created_date": "transfers/transfer/creation_date"
}

mapping2 = {
    "pickup_time": "pickupDate",
    "pickup_address": "originDetails/name",
    "ref_number": "",
    "total_price": "price",
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
    create_csv(chosen_mapping, "test5.csv")
