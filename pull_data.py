import pandas as pd
import sqlite3
import requests

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

excel_url = os.getenv("EXCEL_URL")

# URL of the Excel file
# excel_url = "https://docs.google.com/spreadsheets/d/1EqL3ArudCVWcmJZd2NgC8rK_diIk7dyH4Ws2TRKRBnU/export?format=xlsx"

# Download the Excel file
r = requests.get(excel_url)
with open("temp_excel_file.xlsx", "wb") as f:
    f.write(r.content)

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("data/my_database.db")

# Read the Excel file into a Pandas DataFrame
xls = pd.ExcelFile("temp_excel_file.xlsx")

# Process each sheet in the Excel file
for sheet_name in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name)

    # Write DataFrame to SQLite table
    df.to_sql(sheet_name, conn, if_exists="replace", index=False)

# Close the database connection
conn.close()

# Optionally, remove the downloaded Excel file if it's no longer needed
import os

os.remove("temp_excel_file.xlsx")
