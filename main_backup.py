""" Main xml to csv file:
    This script converts XML files to CSV format, processes data, and manages file organization.
    It includes a GUI built with customtkinter for user interaction. 
"""
import customtkinter as ctk
from tkinter import filedialog
import shutil
import os
from datetime import datetime
import xml.etree.ElementTree as ET
import pandas as pd
import re 

""" Global variables: """
sixSeater = "6 Seater"
sixSeaterPossibilities = ["Private Minivan", "Private Minivan (1-6)", "minivan"]

eightSeater = "8 Seater"
eightSeaterPossibilities = ["Private Minivan (1-8)"]

saloon = "Saloon"
saloonPossibilities = ["Private Transfer", "Private Sedan (1-4)"]

main_folder = "main"
folder_path = f"{main_folder}\input"
output_folder =  f"{main_folder}\output"
processed_folder = f"{main_folder}\processed"
folders = [main_folder, folder_path, output_folder, processed_folder]

time_format = "%H-%M-%S" #Here: Hour-Minute-Second
day_format = "%Y-%m-%d" #Here: Year-Month-Day

data = []

mapping_SUNTR = {   "pickup_time": "transfers/transfer/origin/pickup_time",
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
                    "child_seat_count": "",
                    "booster_seat_count": "",
                    "infant_seat_count": "",
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
                    "created_date": ""
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
                    "child_seat_count": "",
                    "booster_seat_count": "",
                    "infant_seat_count": "",
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
                    "admin_note": "commentary",
                    "ip_address": "",
                    "created_date": ""
}

mapping_excel = {   "pickup_time": ["Fecha", "Hora"],
                    "pickup_address": "Origen",
                    "pickup_address_complete": "",
                    "pickup_latitude": "",
                    "pickup_longitude": "",
                    "dropoff_address": "Destino",
                    "dropoff_address_complete": "",
                    "dropoff_latitude": "",
                    "dropoff_longitude": "",
                    "via_address": "",
                    "via_address_complete": "",
                    "vehicle_type_name": "",
                    "estimated_distance": "",
                    "estimated_duration": "",
                    "ref_number": "Reservera",
                    "total_price": "Neto",
                    "discount_price": "",
                    "discount_code": "",
                    "service_name": "",
                    "service_duration_in_hours": "",
                    "passenger1_name": ["Nombre", "Apellidos"],
                    "passenger1_email": "",
                    "passenger1_phone": "",
                    "passenger2_name": "",
                    "passenger2_email": "",
                    "passenger2_phone": "",
                    "requirements": "",
                    "passenger_count": "PAX",
                    "luggage_count": "",
                    "hand_luggage_count": "",
                    "child_seat_count": "",
                    "booster_seat_count": "",
                    "infant_seat_count": "",
                    "wheelchair_count": "",
                    "pickup_flight_number": "Vuelo",
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
    """ Retrieves a value from an XML element based on the provided path.

        Args:
            path (str or list): Path(s) to the XML element(s).
            root (Element): Root element of the XML tree.

        Returns:
            str: Extracted value or empty string if not found.
    """
    if path == "commentary":
        # Collect all <commentary> elements from anywhere in the XML
        commentary_list = [element.text.strip() for element in root.iter("commentary") if element.text]

        # Join all found commentary entries into a single string
        return "; ".join(commentary_list) if commentary_list else ""

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

def create_csv_SUNTR(mapping, root):
    """ Creates a CSV file for SUNTR reference type, processing specific XML paths.

        Args:
            mapping (dict): Mapping of CSV column names to XML paths.
            file_name (str): Name of the output CSV file.
            root (Element): Root element of the XML tree.
            data (list): List to store rows of data.

        Returns:
            None
    """
    # Find all <transfer> elements under <transfers>
    transfers = root.find("transfers")
    if transfers is None:
        app.printing("No transfers found in this booking.")
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

            elif key == "child_seat_count":
                extras = transfer.find("extras")
                child_seat_count = 0
                if extras is not None:
                    for extra in extras.findall("extra"):
                        name_element = extra.find("name")
                        if name_element is not None and "Child booster seat (2+ years)" in name_element.text:
                            quantity_element = extra.find("quantity")
                            if quantity_element is not None and quantity_element.text.isdigit():
                                child_seat_count += int(quantity_element.text)
                row[key] = str(child_seat_count)

            elif key == "infant_seat_count":
                extras = transfer.find("extras")
                infant_seat_count = 0
                if extras is not None:
                    for extra in extras.findall("extra"):
                        name_element = extra.find("name")
                        if name_element is not None and "Baby Seat (6 - 24 months)" in name_element.text:
                            quantity_element = extra.find("quantity")
                            if quantity_element is not None and quantity_element.text.isdigit():
                                infant_seat_count += int(quantity_element.text)
                row[key] = str(infant_seat_count)
            
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
                elif key == "vehicle_type_name" and entry in eightSeaterPossibilities:
                    entry = eightSeater
                
                elif key == "ref_number":
                    entry += appendix_ref_number
                
                elif key == "passenger1_name":
                    old_entry = entry
                    entry = f"ST - {old_entry}"
                
                elif key == "pickup_flight_number":
                    flight_number = get_item("flight/flight_number", transfer.find("origin"))
                    airline = get_item("flight/airline", transfer.find("origin"))
                    
                    # Extract only the airline code (letters inside brackets)
                    airline_code = ""
                    if airline:
                        match = re.search(r"\((\w+)\)", airline)  # Find letters inside ()
                        if match:
                            airline_code = match.group(1)  # Extract the matched code

                    # Combine airline code with flight number
                    if airline_code and flight_number:
                        entry = f"{airline_code}{flight_number}"
                    elif flight_number:
                        entry = flight_number
                    else:
                        entry = ""

                
                row[key] = entry

        data.append(row)

def create_csv_default(mapping, root):
    """ Creates a CSV file for non-SUNTR reference types, processing specific XML paths.

        Args:
            mapping (dict): Mapping of CSV column names to XML paths.
            file_name (str): Name of the output CSV file.
            root (Element): Root element of the XML tree.
            data (list): List to store rows of data.

        Returns:
            None
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
        elif key == "vehicle_type_name" and entry in eightSeaterPossibilities:
            entry = eightSeater
        
        elif key == "passenger1_name":
            old_entry = entry
            entry = f"MT - {old_entry}"
        
        row[key] = entry

    data.append(row)

def read_excel(file_path):
    """ Reads an Excel file, uses the 2nd row as column headers, maps the data, and saves it to CSV.

        Returns:
            None
    """
    try:
        # Load Excel file, setting the second row (index=1) as the header
        excel_df = pd.read_excel(file_path, dtype=str, header=1)  # 1 means "second row as header"

        # Process each row
        for _, row in excel_df.iterrows():
            transformed_row = {}
            for key, value in mapping_excel.items():
                if isinstance(value, list):
                    if key == "passenger1_name":
                        # Combine multiple fields into a single column (e.g., first & last name)
                        full_name = " ".join(
                            row[col] for col in value if col in row and pd.notna(row[col])
                        ).strip()

                        # Prefix with "Name - "
                        transformed_row[key] = f"CV - {full_name}" if full_name else ""
                    else:
                        # Combine multiple fields into a single column (e.g., first & last name)
                        transformed_row[key] = " ".join(
                            row[col] for col in value if col in row and pd.notna(row[col])
                        ).strip()
                else:
                    # Assign a single field if it exists
                    transformed_row[key] = row[value] if value in row and pd.notna(row[value]) else ""
                
            data.append(transformed_row)

        app.printing(f"Successfully converted {file_path} to.")

    except Exception as e:
        app.printing(f"Error converting Excel to CSV: {e}")

def main():
    """ Main function to process XML files and generate CSVs. 
        It organizes processed files into dated folders and 
        handles SUNTR-specific and default mappings.

        Args:
            None

        Returns:
            None
    """
    day = datetime.now().strftime(day_format)
    time = datetime.now().strftime(time_format)
    date = f"{day}_{time}"
    
    if not os.listdir(folder_path):
        app.printing("There are no xml files to be processed")
    else:
        final_folder = os.path.join(processed_folder, day)
        os.makedirs(final_folder, exist_ok=True) 
        
        final_final_folder = os.path.join(final_folder, time)
        os.makedirs(final_final_folder, exist_ok=True) 
        
        output_output_folder = os.path.join(output_folder, day)
        os.makedirs(output_output_folder, exist_ok=True) 
        # Iterate over all files in the folder
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            
            if file_name.endswith(".xml"):
                app.printing(f"\nProcessing file: {file_name}")
                # Parse the XML file
                tree = ET.parse(file_path)
                root = tree.getroot()

                reference = root.find("reference")
                if reference is not None and "SUNTR" in reference.text:
                    app.printing(f"The reference contains SUNTR in {file_name}.")
                    create_csv_SUNTR(mapping_SUNTR, root)
                else:
                    app.printing(f"The reference does not contain SUNTR in {file_name}. Found: {reference.text if reference is not None else 'None'}")
                    create_csv_default(mapping_default, root)            
                
                # Move the processed XML file to the date-named folder
                new_file_path = os.path.join(final_final_folder, file_name)
                shutil.move(file_path, new_file_path)
                app.printing(f"Moved file to: {new_file_path}")
            
            elif file_name.endswith(".xlsx"):
                app.printing(f"\nProcessing file: {file_name}")
                read_excel(file_path)
                
                # Move the processed XML file to the date-named folder
                new_file_path = os.path.join(final_final_folder, file_name)
                shutil.move(file_path, new_file_path)
                app.printing(f"Moved file to: {new_file_path}")
            
            else:
                app.printing(f"Skipping non-XML or xlsx file: {file_name}")
        
        df = pd.DataFrame(data, dtype=object)
        df.to_csv(f"{output_output_folder}/output_{date}.csv", sep=";", index=False, quoting=3)

class App(ctk.CTk):
    """ GUI application for converting XML files to CSV format.

        Attributes:
            navigation_frame (CTkFrame): Sidebar for navigation buttons.
            home_frame (CTkFrame): Main frame for displaying logs and instructions.
            textbox (CTkTextbox): Output textbox for logs and user guidance.
    """
    def __init__(self):
        """ Initializes the application window and sets up the layout and widgets. """
        super().__init__()

        self.title("Convert xmls and xlsxs to one csv")
        self.geometry("750x300")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        
        self.navigation_frame_label = ctk.CTkLabel(
            self.navigation_frame, 
            text="Image Example", 
            compound="left", 
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        
        self.select_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Select Files",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray20"),
            anchor="w",
            command=self.select_files
        )
        self.select_button.grid(row=1, column=0, sticky="ew")
        
        self.action_button = ctk.CTkButton(
            self.navigation_frame, 
            corner_radius=0,
            height=40, 
            border_spacing=10, 
            text="Convert",
            fg_color="transparent",
            text_color=("gray10", "gray90"), 
            hover_color=("gray70", "gray20"),
            anchor="w", 
            command=self.main_process
        )
        self.action_button.grid(row=2, column=0, sticky="ew")
        
        self.output_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Open Output",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray20"),
            anchor="w",
            command=self.open_output
        )
        self.output_button.grid(row=3, column=0, sticky="ew")
        
        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.navigation_frame, 
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event
        )
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")
        
        # create home frame
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_rowconfigure(0, weight=1)
        
        self.textbox = ctk.CTkTextbox(self.home_frame, corner_radius=0)
        self.textbox.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        
        self.select_frame_by_name("home")
        self.show_intro()

    def select_frame_by_name(self, name):
        """ Displays the specified frame by name.

            Args:
                name (str): Name of the frame to display.

            Returns:
                None
        """
        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()

    def change_appearance_mode_event(self, new_appearance_mode):
        """ Changes the appearance mode of the application.

            Args:
                new_appearance_mode (str): Appearance mode ("Light", "Dark", or "System").

            Returns:
                None
        """
        ctk.set_appearance_mode(new_appearance_mode)
    
    def select_files(self):
        """ Opens a file dialog for the user to select XML files, and copies the selected
            files to the input folder.

            Returns:
                None
        """
        # Open file dialog to select files
        file_paths = filedialog.askopenfilenames(
            title="Select Files",
            filetypes=(("All Files", "*.*"),)
        )
        if file_paths:
            for file_path in file_paths:
                self.printing(f"File selected: {file_path}")
                shutil.copy(file_path, folder_path)
            self.printing("All files have been moved successfully.")
    
    def main_process(self):
        """ Triggers the main processing function to convert XML files to CSV and update logs.

            Returns:
                None
        """
        self.printing("Action start:")
        main()
        self.printing("Action end.")

    def open_output(self, event=None):
        """ Opens the output folder in the file explorer.

            Args:
                event (optional): Event object from a button click.

            Returns:
                None
        """
        try:
            if os.name == "nt":
                os.startfile(f"{output_folder}")
        except Exception as e:
            self.printing(f"Error opening output folder: {e}")

    def remove(self):
        """ Removes the most recently added file from the input folder.

            Returns:
                None
        """
        try:
            # Get a list of all files in the input folder
            files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)]
            
            # Check if the folder is empty
            if not files:
                self.printing("The input folder is empty. No files to remove.")
                return

            # Find the most recently modified file
            latest_file = max(files, key=os.path.getmtime)

            # Delete the file
            os.remove(latest_file)
            self.printing(f"Removed the latest file: {os.path.basename(latest_file)}")
        except Exception as e:
            self.printing(f"Error removing the latest file: {e}")

    def show_intro(self):
        """ Displays an introduction message in the application textbox, guiding the user
            on how to use the program.

            Returns:
                None
        """
        intro_message = (
            "Welcome to the XML to CSV Converter!\n\n"
            "This program allows you to process XML files and convert them into structured CSV format.\n"
            "Here's how to use it:\n\n"
            "1. Download the XML files from the E-Mail\n"
            "2. Move them into the input folder, which you can find in the main folder, "
            "which can be found in the dist folder, where the main executable is.\n"
            "3. Click 'Convert' to process the files into a CSV.\n"
            "4. Click 'Open Output' to open the folder, where you can find the CSV.\n"
            "5. You can find the CSV you just created in the folder with todays date.\n"
            "6. Put the output in the import on the dispatch.\n\n"
        )
        self.printing(intro_message)

    def printing(self, text):
        """ Prints messages to both the console and the GUI's output textbox.

            Args:
                text (str): Message to display.

            Returns:
                None
        """
        #print(text)
        self.textbox.configure(state="normal")
        self.textbox.insert("end", f"{text}\n")
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

if __name__ == "__main__":
    """ Entry point of the program. Sets up required folders and starts the GUI. """
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
    app = App()
    app.mainloop()
