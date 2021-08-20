"""
Class ObservationsTxt process spinup_data and forecast_data and write the
formatted Observations.txt file required by AquiModAWS.

Author:
    Brogan McCawley (16/08/2021)
"""

import os
import pandas as pd
from .model import Model
from .functions import check_timeseries_continuity, line_prepender


class ObservationsTxt:
    """
    Class represents the behaviours required to format spinup and forecast
    data, along with initial groundwater levels to create Observations.txt.
    """
    def __init__(self, model: Model):
        """Takes only Model as input and extracts data into attributes."""
        self.model = model
        self.model_path = model.model_path
        self.catchment = model.catchment
        self.spinup_data = model.spinup_data
        self.forecast_data = model.forecast_data
        self.spinup_init_GWL = model.spinup_init_GWL
        self.forecast_init_GWL = model.forecast_init_GWL
        self.processed_data: pd.DataFrame = pd.DataFrame()

    def process_data(self):
        """
        Process spinup and forecast data into the Observations.txt file format.
        Saves the spinup period length to Model for use with Input.txt.
        """
        forecast_start_date = self.forecast_data.index[0]
        spinup_sliced = self.spinup_data.loc[
            :forecast_start_date - pd.Timedelta(days=1)
        ]
        df = pd.concat([spinup_sliced, self.forecast_data]).sort_index()
        check_timeseries_continuity(df)
        self.model.spinup_period = len(spinup_sliced.index)
        df['DAY'] = df.index.to_series().dt.day
        df['MONTH'] = df.index.to_series().dt.month
        df['YEAR'] = df.index.to_series().dt.year
        df['GWL'] = "-9999"
        df['ABS'] = 0
        df['SM'] = "-9999"
        df[''] = ''
        df.loc[df.index[0], 'GWL'] = self.spinup_init_GWL
        df.loc[forecast_start_date, "GWL"] = self.forecast_init_GWL
        df.loc[forecast_start_date, ""] = "*"
        df = df[
            ['DAY', 'MONTH', 'YEAR', 'RAIN', 'PET', 'GWL', 'ABS', 'SM', '']
        ]
        self.processed_data = df

    def write_file(self):
        """Write formatted data to Observations.txt"""
        filepath = os.path.join(self.model_path, "Observations.txt")
        self.processed_data.to_csv(
            filepath,
            sep="\t",
            index=False
        )
        num_of_obs = len(self.processed_data.index)
        to_prepend = f"NUMBER OF OBSERVATIONS\n{num_of_obs}"
        line_prepender(filepath, to_prepend)
