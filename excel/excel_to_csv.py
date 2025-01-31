import pandas as pd
import os

mapping_excel = {   "pickup_time": "",
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
                    "vehicle_type_name": "",
                    "estimated_distance": "",
                    "estimated_duration": "",
                    "ref_number": "",
                    "total_price": "price",
                    "discount_price": "",
                    "discount_code": "",
                    "service_name": "",
                    "service_duration_in_hours": "",
                    "passenger1_name": "",
                    "passenger1_email": "",
                    "passenger1_phone": "",
                    "passenger2_name": "",
                    "passenger2_email": "",
                    "passenger2_phone": "",
                    "requirements": "",
                    "passenger_count": "",
                    "luggage_count": "",
                    "hand_luggage_count": "",
                    "child_seat_count": "",
                    "booster_seat_count": "",
                    "infant_seat_count": "",
                    "wheelchair_count": "",
                    "pickup_flight_number": "",
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

excel_df = pd.read_excel(f"{main_path}/listado.xls", dtype=str, engine='xlrd')

print(excel_df)
#print(f"Vehicle Type: {excel_df.at[0, "Vehicle Type"]}")
