import xml.etree.ElementTree as ET

def parse_element(element, level=0):
    """
    Recursively parse an XML element and print its tag, attributes, and text.
    """
    indent = "  " * level
    print(f"{indent}Tag: {element.tag}, Attributes: {element.attrib}")

    # Print text content if present
    if element.text and element.text.strip():
        print(f"{indent}  Text: {element.text.strip()}")
        list.append([element.tag, element.text.strip()])

    # Recursively parse child elements
    for child in element:
        parse_element(child, level + 1)

# Load and parse the XML file
file_path = 'Python/Praktikum/booking_4092840.xml'
tree = ET.parse(file_path)
root = tree.getroot()

list = []

# Parse and print all information
print("XML Content:")
parse_element(root)
#print(list)

for item in list: 
    print(item)

print(f"\n{list[0]}")
