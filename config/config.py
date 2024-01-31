import datetime
from dotenv import load_dotenv
import os
import logging

from util.decide_date_range import decide_date_range

load_dotenv()

dateRange = decide_date_range(datetime.date.today())

Config = {
    # "start_date": datetime.date(2023, 12, 1),
    # "end_date": datetime.date(2023, 12, 31),
    "start_date": dateRange.start_date,
    "end_date": dateRange.end_date,
    "max_value_to_include": 100_000,
    "spreadsheet_tab_name": "This_Month",
    "spreadsheet_index": 1, # a zero-based index, meaning the first tab is 0
    "spreadsheet_id": os.getenv("SHEETS_SPREADSHEET_ID"),
    "google_credentials": {
        "private_key": os.getenv("SHEETS_PRIVATE_KEY"),
        "client_email": os.getenv("SHEETS_SVC_ACCOUNT"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
    },
    "plaid": {
        "client_id": os.getenv("PLAID_CLIENT_ID"),
        "secret": os.getenv("PLAID_SECRET"),
        "env": os.getenv("PLAID_ENV"),
        "version": "2020-09-14",
    },
    "log_level": logging.INFO,
}
