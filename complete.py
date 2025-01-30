import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import filedialog
import shutil
import os
from datetime import datetime
import xml.etree.ElementTree as ET
import pandas as pd


"""Global variables:"""
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



def get_item(path, root):
    """
    Extracts the value from the XML path. Supports both single paths (string)
    and multiple paths (list).
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

def create_csv_SUNTR(mapping, file_name, root, data):
    """
    Creates a DataFrame from the mapping and appends data for all transfers to the CSV.
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
                
                elif key == "source_name":
                    entry = "Sun Transfers"
                
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
        elif key == "vehicle_type_name" and entry in eightSeaterPossibilities:
            entry = eightSeater
        
        row[key] = entry

    # Append the row for this transfer
    data.append(row)

    # Save to CSV
    df = pd.DataFrame(data, dtype=object)
    df.to_csv(file_name, sep=";", index=False, quoting=3)

def main():
    # Initialize the shared dataset
    data = []

    # Create the output folder with the current date
    date = datetime.now().strftime(date_format)
    

    if not os.listdir(folder_path):
        app.printing("There are no xml files to be processed")
    else:   
        final_folder = os.path.join(processed_folder, date)
        os.makedirs(final_folder, exist_ok=True) 
        # Iterate over all files in the folder
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
        
            # Check if it's an XML file
            if not file_name.endswith(".xml"):
                app.printing(f"Skipping non-XML file: {file_name}")
                continue

            app.printing(f"\nProcessing file: {file_name}")

            # Parse the XML file
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Determine the mapping based on the reference
            reference = root.find("reference")
            if reference is not None and "SUNTR" in reference.text:
                app.printing(f"The reference contains SUNTR in {file_name}.")
                create_csv_SUNTR(mapping_SUNTR, f"{output_folder}/output_{date}.csv", root, data)
            else:
                app.printing(f"The reference does not contain SUNTR in {file_name}. Found: {reference.text if reference is not None else 'None'}")
                create_csv_default(mapping_default, f"{output_folder}/output_{date}.csv", root, data)

            # Extract data and append it as a new row
            
            
            # Move the processed XML file to the date-named folder
            new_file_path = os.path.join(final_folder, file_name)
            shutil.move(file_path, new_file_path)
            app.printing(f"Moved file to: {new_file_path}")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set up the CTk window
        self.title("Convert xmls to csvs")
        self.geometry("700x450")
        
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
            hover_color=("gray70", "gray30"),
            anchor="w", 
            command=self.on_button_click
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
            hover_color=("gray70", "gray30"),
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
        #self.textbox.configure(state="disabled")
        
        self.select_frame_by_name("home")
        
        self.show_intro()

    def select_frame_by_name(self, name):
        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
    
    def home_button_event(self):
        self.select_frame_by_name("home")

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
    
    def select_files(self):
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
    
    def on_button_click(self):
        self.printing("Action start:")
        main()
        self.printing("Action end.")

    def open_output(self, event=None):
        try:
            if os.name == "nt":  # Windows
                os.startfile(output_folder)
        except Exception as e:
            self.printing(f"Error opening output folder: {e}")

    def show_intro(self):
        """
        Displays an introduction message in the CTkTextbox when the application starts.
        """
        intro_message = (
            "Welcome to the XML to CSV Converter!\n\n"
            "This program allows you to process XML files and convert them into structured CSV format.\n"
            "Here's how to use it:\n\n"
            "1. Click 'Select Files' to choose XML files.\n"
            "2. Click 'Convert' to process and extract data into CSV.\n"
            "3. The processed files will be saved in the 'output' folder, while the original XML files "
            "will be copied to the 'processed' folder and you can open the 'output' folder by clicking "
            "on the 'OpenOutput' button.\n\n"
        )
        self.printing(intro_message)

    def printing(self, text):
        print(text)
        self.textbox.configure(state="normal")
        self.textbox.insert("end", f"{text}\n")
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

if __name__ == "__main__":
    os.makedirs(main_folder, exist_ok=True)
    os.makedirs(f"{folder_path}", exist_ok=True)
    os.makedirs(f"{output_folder}", exist_ok=True)
    os.makedirs(f"{processed_folder}", exist_ok=True)
    #shutil.copy("complete.py", main_folder)
    app = App()
    app.mainloop()
