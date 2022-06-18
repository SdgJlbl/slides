from sklearn.metrics import confusion_matrix
import numpy as np
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from typing import Protocol


def update_confusion_matrix(current_confusion_matrix, y_true, y_pred):
    conf_mat = confusion_matrix(y_true, y_pred)
    return conf_mat + current_confusion_matrix


class SpreadSheet(Protocol):
    def load(self) -> np.array:
        ...

    def dump(self, data: np.array):
        ...


def main(spreadsheet: SpreadSheet, y_true: np.array, y_pred: np.array):
    old_confusion_matrix = spreadsheet.load()
    new_confusion_matrix = update_confusion_matrix(old_confusion_matrix, y_true, y_pred)
    spreadsheet.dump(new_confusion_matrix)


class GSpreadSheet:
    def __init__(self, credentials, gsheet_name, worksheet_name, area):
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials)
        self.client = gspread.authorize(creds)
        self.spreadsheet = self.client.open(gsheet_name)
        self.worksheet = self.spreadsheet.worksheet(worksheet_name)
        self.area = area

    def load(self):
        return np.array(self.worksheet.get(self.area))

    def dump(self, data):
        self.worksheet.update(self.area, data.tolist())


class ExcelSpreadSheet:
    def __init__(self, local_path, worksheet_name):
        self.local_path = local_path
        self.worksheet_name = worksheet_name

    def load(self):
        return pd.read_excel(
            self.local_path, sheet_name=self.worksheet_name, index_col=0, header=0
        ).values

    def dump(self, data):
        current_df = pd.read_excel(
            self.local_path, sheet_name=self.worksheet_name, index_col=0, header=0
        )
        new_df = pd.DataFrame(data, index=current_df.index, columns=current_df.columns)
        new_df.to_excel(self.local_path, sheet_name=self.worksheet_name)
