from dotenv import load_dotenv
import os
import logging

load_dotenv()


Config = {
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "max_value_to_include": 100_000,
    "spreadsheet_tab_name": "This_Month",
    "spreadsheet_id": "",
    "google_credentials": {
        "private_key": os.getenv("SHEETS_PRIVATE_KEY"),
        "client_email": os.getenv("SHEETS_SVC_ACCOUNT"),
    },
    "plaid": {
        "client_id": os.getenv("PLAID_CLIENT_ID"),
        "secret": os.getenv("PLAID_SECRET"),
        "env": os.getenv("PLAID_ENV"),
    },
    "log_level": logging.DEBUG,
}
