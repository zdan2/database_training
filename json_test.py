import gspread
from google.oauth2.service_account import Credentials

CREDS_JSON = "app/secrets/service_account.json"
SPREADSHEET_ID = "12DsHjyslvx8Nw5QFayqWFg1tv8ggdCjW1cLxR_tWOjc"
WORKSHEET_TITLE = "シート1"

scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
creds = Credentials.from_service_account_file(CREDS_JSON, scopes=scopes)

gc = gspread.authorize(creds)
sh = gc.open_by_key(SPREADSHEET_ID)
ws = sh.worksheet(WORKSHEET_TITLE)

print(ws.get_all_records()[:3])  # 先頭3行を表示