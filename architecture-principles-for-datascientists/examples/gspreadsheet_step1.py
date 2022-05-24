import gspread_dataframe


def update_data(client, gsheet_name, metrics, confusion_matrix):
    gspreadsheet = client.open(gsheet_name)


    # Map sheet name to worksheet object
    worksheet_dict = {sheet.title: sheet for sheet in gspreadsheet.worksheets()}

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
