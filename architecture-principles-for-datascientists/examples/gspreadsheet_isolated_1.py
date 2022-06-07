import gspread
from gspread_dataframe import set_with_dataframe, get_as_dataframe
from oauth2client.service_account import ServiceAccountCredentials
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential
import dataclasses
import pandas as pd


@dataclasses.dataclass
class WorksheetUpdate:
    name: str
    contents: pd.DataFrame
    update: bool = False


class GsheetWriter:
    def __init__(self, google_keyfile_dict, gsheet_name):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            keyfile_dict=google_keyfile_dict,
            scopes=["https://www.googleapis.com/auth/spreadsheets"],
        )
        self.client = gspread.authorize(self.credentials)
        self.gsheet_name = gsheet_name
        self._gsheet = None

    @property
    def gsheet(self):
        return self._gsheet or self.open_gsheet()

    def open_gsheet(self):
        try:
            self._gsheet = self.client.open(self.gsheet_name)  # Open the Google Sheet
        except gspread.SpreadsheetNotFound:
            raise gspread.SpreadsheetNotFound(
                "Have you shared your sheet with the client_email in the credentials file?"
            )
        return self._gsheet

    def update_worksheet(self, *, worksheet_name, worksheet_content, update=False):
        gsheet = self.gsheet
        try:
            worksheet = gsheet.worksheet(worksheet_name)
        except gspread.exceptions.WorksheetNotFound:
            rows, cols = worksheet_content.shape
            worksheet = gsheet.add_worksheet(
                title=worksheet_name, rows=str(rows), cols=str(cols)
            )

        if update:
            current_content = get_as_dataframe(worksheet)
            updated_content = current_content + worksheet_content
            set_with_dataframe(worksheet, updated_content, resize=True)
        else:
            set_with_dataframe(worksheet, worksheet_content, resize=True)


def update_data(writer, metrics, confusion_matrix):
    worksheet_updates = [
        WorksheetUpdate(
            name="Confusion matrix",
            contents=confusion_matrix,
            update=True,
        ),
        WorksheetUpdate(name="Metrics", contents=metrics),
    ]
    for worksheet_update in worksheet_updates:
        writer.update_worksheet(worksheet_update=worksheet_update)


def main():
    writer = GsheetWriter(credentials, gsheet_name)
    update_data(writer, metrics, confusion_matrix)
