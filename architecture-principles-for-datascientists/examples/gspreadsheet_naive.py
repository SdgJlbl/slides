import gspread, gspread_dataframe
from oauth2client.service_account import ServiceAccountCredentials


def update_data(gsheet_name, metrics, confusion_matrix):
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scope=["https://www.googleapis.com/auth/spreadsheets"]
    )
    client = gspread.authorize(creds)

    try:
        gspreadsheet = client.open(gsheet_name)
    except gspread.exceptions.SpreadsheetNotFound as e:
        raise Exception(
            "Spreadsheet not found, Please check permissions", e
        )

    # Map sheet name to worksheet object
    worksheet_dict = {
        sheet.title: sheet for sheet in gspreadsheet.worksheets()}

    # update confusion matrix
    current_conf_mat = gspread_dataframe.get_as_dataframe(worksheet_dict["Confusion matrix"])
    new_conf_mat = confusion_matrix + current_conf_mat
    gspread_dataframe.set_with_dataframe(
        worksheet_dict["Confusion matrix"], new_conf_mat, resize=True
    )

    # save metrics
    worksheet_dict["Metrics"].clear()
    gspread_dataframe.set_with_dataframe(
        worksheet_dict["Metrics"], metrics, resize=True
    )
