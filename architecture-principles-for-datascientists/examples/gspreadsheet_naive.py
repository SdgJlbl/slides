import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sklearn.metrics import confusion_matrix
import numpy as np


def update_confusion_matrix(gsheet_name, y_true, y_pred):
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json")
    client = gspread.authorize(creds)
    gspreadsheet = client.open(gsheet_name)
    worksheet = gspreadsheet.worksheet("Confusion matrix")

    # get current values
    current_conf_mat = np.array(worksheet.get(area="B2:D4"))

    # update confusion matrix
    conf_mat = confusion_matrix(y_true, y_pred)
    new_conf_mat = conf_mat + current_conf_mat

    # save confusion matrix
    worksheet.update(area="B2:D4", values=new_conf_mat.to_list())


def main(gsheet_name, y_true, y_pred):
    update_confusion_matrix(gsheet_name, y_true, y_pred)
