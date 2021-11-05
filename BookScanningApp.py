from Price_check import price
import time
from googleapiclient.discovery import build
from google.oauth2 import service_account



SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'
creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
SAMPLE_SPREADSHEET_ID = 'Spreadsheet ID'
service = build('sheets', 'v4', credentials=creds)
# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="3 sorted!A2:A100").execute()
values = result.get('values', [])



def main():

    x=5
    while 1: 
        print(x)
        sheet = service.spreadsheets()
        range = "Sheet9!A"+str(x)
        #print(range)
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range).execute()
        values = result.get('values')
        
        print(values)
        if str(values)=='None':
            time.sleep(2)

        else:
            values=values[0]
            price(values,x)
            x=x+1
            
            time.sleep(10)



if __name__ == "__main__":
    main()

