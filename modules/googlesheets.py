from gspread import Client, Spreadsheet, Worksheet, service_account
from loguru import logger
import pandas as pd
from time import time
from config import GOOGLE_SHEETS_CONFIG_FILE, GOOGLE_SHEET_URL


class GoogleSheets:
    def __init__(self, page_name: str):
        logger.info("Initializing Google Sheets for page: {}", page_name)
        if GOOGLE_SHEET_URL != '':
            self.gc: Client = service_account(filename=GOOGLE_SHEETS_CONFIG_FILE)
            self.sh: Spreadsheet = self.gc.open_by_url(GOOGLE_SHEET_URL)
            self.ws: Worksheet = self.sh.worksheet(page_name)
            self.sheet_name = page_name
        else:
            self.gc, self.sh, self.ws, self.sheet_name = None, None, None, None
            logger.warning("Google Sheets URL is not specified.")

    def clear_worksheet(self):
        if self.ws:
            logger.info("Clearing worksheet: {}", self.sheet_name)
            self.ws.clear()

    def update_worksheet(self, df: pd.DataFrame, batch_size: int = 1000):
        start_time = time()
        if self.ws:
            logger.info("Updating worksheet: {} with {} rows", self.sheet_name, len(df))
            self.clear_worksheet()
            self.ws.append_row(df.columns.values.tolist())
            for start_row in range(0, len(df), batch_size):
                end_row = min(start_row + batch_size, len(df))
                data_batch = df.iloc[start_row:end_row].values.tolist()
                self.ws.append_rows(data_batch)
            end_time = time()
            logger.info("Data successfully updated in Google Sheets in {:.2f} seconds", end_time - start_time)
