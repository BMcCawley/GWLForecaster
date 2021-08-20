"""
InputData class.

Author:
    Brogan McCawley (16/08/2021)
"""

import pandas as pd
from .model import Model


class InputData:
    """
    InputData is a class to read and parse the timeseries data required to
    create the Observations.txt file required by AquiModAWS. It parses spinup
    and forecast data and saves these to the original single model, accessed
    by self.model. Note that the object saved at self.model is not a copy of
    original Model object, but the actualy object itself. Therefore altering
    attributes via self.model alters the attributes of the Model instance
    everywhere.
    """
    def __init__(self, model: Model):
        """Take Model as an argument and extract data."""
        self.model = model
        self.filepath = model.input_form_path
        self.identifier = model.identifier
        self.raw_data = pd.read_excel(
            model.input_form_path,
            sheet_name=model.identifier
        )

    def parse_spinup_data(self):
        """Parse and extract the spinup data."""
        spinup_data = self.raw_data[[
            'spinup_DATE', 'spinup_RAIN', 'spinup_PET'
        ]]
        spinup_data = spinup_data.dropna()
        spinup_data = spinup_data.set_index('spinup_DATE', drop=True)
        # Make sure datetime format is recognised
        spinup_data.index = pd.to_datetime(spinup_data.index)
        # Convert every date to midnight, in case there is a time component
        spinup_data.index = spinup_data.index.normalize()
        spinup_data = spinup_data.rename(
            columns={'spinup_RAIN': 'RAIN', 'spinup_PET': 'PET'}
        )
        self.model.spinup_data = spinup_data

    def parse_forecast_data(self):
        """Parse and extract the forecast data."""
        forecast_data = self.raw_data[[
            'forecast_DATE', 'forecast_RAIN', 'forecast_PET'
        ]]
        forecast_data = forecast_data.dropna()
        forecast_data = forecast_data.set_index('forecast_DATE', drop=True)
        # Make sure datetime format is recognised
        forecast_data.index = pd.to_datetime(forecast_data.index)
        # Convert every date to midnight, in case there is a time component
        forecast_data.index = forecast_data.index.normalize()
        forecast_data = forecast_data.rename(
            columns={'forecast_RAIN': 'RAIN', 'forecast_PET': 'PET'}
        )
        self.model.forecast_data = forecast_data
