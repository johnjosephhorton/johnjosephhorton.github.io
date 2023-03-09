# imports

import pandas as pd

import gspread
from oauth2client.service_account import ServiceAccountCredentials

import json

with open('key.json', 'r') as f:
    config = json.load(f)
	
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
	
# credential object for authenticating
creds_obj = ServiceAccountCredentials.from_json_keyfile_dict(config, scope)
	
client = gspread.authorize(creds_obj)

sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1EqL3ArudCVWcmJZd2NgC8rK_diIk7dyH4Ws2TRKRBnU/edit#gid=0")	

medatadata = sheet.fetch_sheet_metadata()

for worksheet in sheet.worksheets():
    title = worksheet.title
    data = worksheet.get_all_values()
    df = pd.DataFrame(data)    
    df.to_csv(f'data/{title}.csv', index=False, header=False)



