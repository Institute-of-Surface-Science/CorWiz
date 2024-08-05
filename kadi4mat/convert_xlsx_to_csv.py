import pandas as pd

# Load the Excel file
file_name = '../data/tables/a_general_corrosion_function_in_terms_of_atmospher_tables'
excel_file = file_name + '.xlsx'

# Read the Excel file
excel_data = pd.ExcelFile(excel_file, engine='openpyxl')

# Iterate through each sheet and save it as a CSV file
for sheet_name in excel_data.sheet_names:
    df = pd.read_excel(excel_file, sheet_name=sheet_name, engine='openpyxl')
    df.to_csv(file_name + '_' + f'{sheet_name}.csv', index=False)

print("Conversion complete.")