import pandas as pd
import re

# Input and output file names
input_file = r"C:\Users\YaseenHussain\Documents\EV Charger\EV India Penetration\EV India Maker List 2020.xlsx"
output_file = r"C:\Users\YaseenHussain\Documents\EV Charger\EV India Penetration\EV India Maker List 2020_splited.xlsx"

# Read the Excel file
df = pd.read_excel(input_file)

# Strip spaces from headers
df.columns = df.columns.str.strip()

# Get first two columns (S. No. and Maker)
col_a, col_b = df.columns[0], df.columns[1]

def clean_sheet_name(name):
    # Remove invalid Excel characters and limit to 30 chars
    return re.sub(r'[:\\/?*\[\]]', '', str(name))[:30]

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    for col in df.columns[2:]:
        temp = df[[col_a, col_b, col]].copy()

        # Keep only rows with value > 0
        temp = temp[temp[col] > 0]

        if temp.empty:
            continue

        # Sort descending by this category
        temp = temp.sort_values(by=col, ascending=False)

        # Clean the sheet name
        sheet_name = clean_sheet_name(col)

        # Write to Excel
        temp.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"✅ Split file created: {output_file}")
