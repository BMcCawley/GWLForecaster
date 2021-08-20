"""
Class Executor to execute AquiModAWS

Author:
    Brogan McCawley (16/08/2021)
"""

import os
from .model import Model


class Executor:
    """Class to execute AquiModAWS."""
    def __init__(self, model: Model):
        """
        Takes Model as the only constructor argument.
        self.output_path is the path where AquiModAWS output files are saved.
        self.path is the path where the AquiModAWS calibrated parameters,
        configuration and data files are saved.
        """
        self.path = model.model_path
        self.output_path = os.path.join(model.model_path, "Output")

    def clear_output_directory(self):
        """Delete all files in the AquiModAWS output directory."""
        files = os.listdir(self.output_path)
        if len(files) != 0:
            for f in files:
                os.remove(os.path.join(self.output_path, f))

    def execute(self):
        """Execute AquiModAWS."""
        os.system("AquiModAWS " + self.path)
