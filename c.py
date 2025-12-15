import gspread
from google.oauth2.service_account import Credentials


SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

def open_sheet(creds_json_path: str, spreadsheet_id: str, worksheet_title: str):
    creds = Credentials.from_service_account_file(creds_json_path, scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(spreadsheet_id)
    ws = sh.worksheet(worksheet_title)
    return ws