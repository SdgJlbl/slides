import pandas as pd


class ExcelWriter:
    """
    Interface layer to abstract away details of local Excel file implementation

    Parameters
    ----------
    local_path: str
    """

    def __init__(self, local_path):
        self.local_path = local_path

    def update_worksheet(self, *, worksheet_update: WorksheetUpdate):
        if worksheet_update.update:
            current_content = pd.read_excel(
                self.local_path, sheet_name=worksheet_update.name
            )
            updated_content = current_content + worksheet_update.contents
            updated_content.to_excel(self.local_path, sheet_name=worksheet_update.name)
        else:
            worksheet_update.contents.to_excel(
                self.local_path, sheet_name=worksheet_update.name
            )
