"""
Load data from the Summary tab of Input_Form.xlsx and represent as InputForm.

Author:
    Brogan McCawley 16/08/2021
"""

import pandas as pd
from .model_resources.exceptions import SeriesNotUniqueError


class InputForm:
    """Read User_Input.xlsx"""
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.data = pd.read_excel(filepath, sheet_name="Summary")

    def check_unique_id(self):
        if not self.data['ID'].unique:
            raise SeriesNotUniqueError(
                "Make sure Input_Form.xlsx IDs are unique"
            )
