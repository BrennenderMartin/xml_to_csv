import pandas as pd
import os

mapping_excel = {   "pickup_time": ["Fecha", "Hora"],
                    "pickup_address": "",
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

main_path = "excel"
excel_file_path = os.path.join(main_path, "listado.xlsx")
output_csv_path = os.path.join(main_path, "output.csv")

def read_excel():
    """
    Reads an Excel file, uses the 2nd row as column headers, maps the data, and saves it to CSV.

    Returns:
        None
    """
    try:
        # Load Excel file, setting the second row (index=1) as the header
        excel_df = pd.read_excel(excel_file_path, dtype=str, header=1)  # 1 means "second row as header"

        # Prepare an empty list to store transformed data
        data = []

        # Process each row
        for _, row in excel_df.iterrows():
            transformed_row = {}
            for key, value in mapping_excel.items():
                if isinstance(value, list):
                    # Combine multiple fields into a single column (e.g., first & last name)
                    transformed_row[key] = " ".join(
                        row[col] for col in value if col in row and pd.notna(row[col])
                    ).strip()
                else:
                    # Assign a single field if it exists
                    transformed_row[key] = row[value] if value in row and pd.notna(row[value]) else ""

            data.append(transformed_row)

        # Convert the list into a DataFrame and save to CSV
        df = pd.DataFrame(data, dtype=object)
        df.to_csv(output_csv_path, sep=";", index=False, quoting=3)

        print(f"Successfully converted {excel_file_path} to {output_csv_path}.")

    except Exception as e:
        print(f"Error converting Excel to CSV: {e}")

#print(excel_df)
read_excel()
#print(f"Vehicle Type: {excel_df.at[0, "Vehicle Type"]}")
