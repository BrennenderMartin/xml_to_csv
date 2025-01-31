import pandas as pd
import os

main_path = "excel"

excel_df = pd.read_excel(f"{main_path}/test1.xlsx", dtype=str)

print(excel_df)
print(f"Vehicle Type: {excel_df.at[0, "Vehicle Type"]}")
