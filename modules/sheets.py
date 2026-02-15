import gspread
import os
import logging
from datetime import datetime

class SheetsModule:
    def __init__(self):
        self.creds_file = os.getenv("GOOGLE_CREDENTIALS_FILE", "google_credentials.json")
        self.sheet_url = os.getenv("SHEET_URL")
        self.client = None
        self.sheet = None
        
        self._authenticate()

    def _authenticate(self):
        try:
            if os.path.exists(self.creds_file) and self.sheet_url:
                self.client = gspread.service_account(filename=self.creds_file)
                self.sheet = self.client.open_by_url(self.sheet_url)
                logging.info("✅ Connected to Google Sheets")
            else:
                logging.warning(f"⚠️ Google Sheets credentials not found at {self.creds_file} or URL missing. Sync disabled.")
        except Exception as e:
            logging.exception(f"❌ Failed to connect to Google Sheets: {e}")

    def append_event(self, event_data: dict):
        if not self.sheet: return
        try:
            worksheet = self._get_or_create_worksheet("Events")
            row = [
                str(event_data.get("start_time")),
                event_data.get("title"),
                str(event_data.get("user_id")),
                str(datetime.utcnow())
            ]
            worksheet.append_row(row)
        except Exception as e:
            logging.error(f"❌ Failed to sync event to Sheets: {e}")

    def append_expense(self, expense_data: dict):
        if not self.sheet: return
        try:
            worksheet = self._get_or_create_worksheet("Expenses")
            row = [
                str(expense_data.get("date", datetime.utcnow())),
                expense_data.get("category"),
                expense_data.get("amount"),
                expense_data.get("description"),
                str(expense_data.get("user_id"))
            ]
            worksheet.append_row(row)
        except Exception as e:
            logging.error(f"❌ Failed to sync expense to Sheets: {e}")

    def _get_or_create_worksheet(self, title):
        try:
            return self.sheet.worksheet(title)
        except gspread.WorksheetNotFound:
            return self.sheet.add_worksheet(title=title, rows=100, cols=10)
