import xml.etree.ElementTree as ET

def parse_element(element, level=0, parent_tag=None):
    """
    Recursively parse an XML element, print its tag, attributes, and text,
    and store it in a list with context (parent tag).
    """
    indent = "  " * level
    print(f"{indent}Tag: {element.tag}, Attributes: {element.attrib}")

    # Print text content if present
    if element.text and element.text.strip():
        print(f"{indent}  Text: {element.text.strip()}")
        data_list.append({
            "parent": parent_tag,
            "tag": element.tag,
            "text": element.text.strip(),
            "attributes": element.attrib
        })

    # Recursively parse child elements, passing current tag as the parent
    for child in element:
        parse_element(child, level + 1, parent_tag=element.tag)

# Load and parse the XML file
file_path = 'Python/Praktikum/booking_4092840.xml'
tree = ET.parse(file_path)
root = tree.getroot()

data_list = []

# Parse and print all information
print("XML Content:")
parse_element(root)

# Display structured data
print("\nExtracted Data:")
for item in data_list:
    print(item)

# Example: Differentiating customer and passenger names

def get_item(parent, tag):
    item = next((item['text'] 
                for item in data_list 
                if item['tag'] == tag and 
                item['parent'] == parent), None)
    
    return {tag, item}

#customer_name = next((item['text'] for item in data_list if item['tag'] == 'name' and item['parent'] == 'customer'), None)
#passenger_name = next((item['text'] for item in data_list if item['tag'] == 'name' and item['parent'] == 'lead_passenger'), None)

customer_name = get_item("customer", "name")
passenger_name = get_item("lead_passenger", "name")

item = get_item("booking", "reference")
print(item)

print("\nSpecific Information:")
print(f"Customer Name: {customer_name}")
print(f"Passenger Name: {passenger_name}")
