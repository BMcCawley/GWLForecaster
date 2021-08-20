"""
Class InputTxt modifies a preconfigured Input.txt file.

Author:
    Brogan McCawley (16/08/2021)
"""

import os
from .model import Model


class InputTxt:
    """Class to modify a preconfigured Input.txt file."""
    def __init__(self, model: Model):
        """Takes only Model as input and extract data."""
        self.filepath = os.path.join(model.model_path, "Input.txt")
        self.num_runs = model.num_runs
        self.spinup_period = model.spinup_period

    def edit_file(self):
        """
        Edit the number of runs and spinup period according to data parsed from
        User_Input.xlsx.
        """
        with open(self.filepath, 'r') as f:
            lines = f.readlines()
            lines[10] = str(self.num_runs) + "\n"
            lines[16] = str(self.spinup_period) + "\n"

        with open(self.filepath, 'w') as f:
            f.writelines(lines)
