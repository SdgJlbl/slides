from sklearn.metrics import confusion_matrix
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def update_confusion_matrix(current_confusion_matrix, y_true, y_pred):
    conf_mat = confusion_matrix(y_true, y_pred)
    return conf_mat + current_confusion_matrix


def load_confusion_matrix(worksheet, area):
    return np.array(worksheet.get(area))


def save_confusion_matrix(worksheet, data, area):
    worksheet.update(area, data.tolist())


def open_gworksheet():
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json")
    client = gspread.authorize(creds)
    gspreadsheet = client.open("gsheet_name")
    return gspreadsheet.worksheet("Confusion matrix")


def main(y_true, y_pred):
    worksheet = open_gworksheet()
    area = "B2:D4"
    old_confusion_matrix = load_confusion_matrix(worksheet, area)
    new_confusion_matrix = update_confusion_matrix(old_confusion_matrix, y_true, y_pred)
    save_confusion_matrix(worksheet, new_confusion_matrix, area)
