import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sklearn.metrics import confusion_matrix
import numpy as np


def load_confusion_matrix(gsheet_name):
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json")
    client = gspread.authorize(creds)
    gspreadsheet = client.open(gsheet_name)
    worksheet = gspreadsheet.worksheet("Confusion matrix")
    return np.array(worksheet.get("B2:D4"))


def save_confusion_matrix(gsheet_name, data):
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json")
    client = gspread.authorize(creds)
    gspreadsheet = client.open(gsheet_name)
    worksheet = gspreadsheet.worksheet("Confusion matrix")
    worksheet.update("B2:D4", data.tolist())


def update_confusion_matrix(current_confusion_matrix, y_true, y_pred):
    conf_mat = confusion_matrix(y_true, y_pred)
    return conf_mat + current_confusion_matrix


def main(y_true, y_pred):
    gsheet_name = "foobar"
    old_confusion_matrix = load_confusion_matrix(gsheet_name)
    new_confusion_matrix = update_confusion_matrix(old_confusion_matrix, y_true, y_pred)
    save_confusion_matrix(gsheet_name, new_confusion_matrix)
