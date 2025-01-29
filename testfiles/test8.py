def get_item(path):
    element = root.find(path)
    if element is not None and element.text:
        return element.text.strip()
    return "None"

def create_csv(mapping):
    data = []  # Store rows of data (each as a dictionary)
    
    # Prepare one row with all key-value pairs
    row = {}
    for key, value in mapping.items():
        entry = get_item(value)  # Extract value for the key
        row[key] = entry  # Add to the row
    
    data.append(row)  # Append the row to the data list
    data.append(row)  # Adding the same row twice for demonstration purposes

    # Create the DataFrame with two rows
    csv_df = pd.DataFrame(data)
    print(csv_df)

# Example Mapping and Usage
mapping = {
    "Pickup Time": "transfers/transfer/origin/pickup_time",
    "Origin Type": "transfers/transfer/origin",
    "Destination": "transfers/transfer/destination/name",
}

# Assuming root is already parsed from your XML
create_csv(mapping)
