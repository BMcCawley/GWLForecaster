"""
Class OutputData parses the output of AquiModAWS on a model-by-model basis and
creates a tidy CSV file with the data.

Author:
    Brogan McCawley (16/08/2021)
"""

import os
import pandas as pd
from .model import Model


class OutputData:
    """
    Contains the data and behaviour for loading, processing and writing out
    AquiModAWS output data.
    """
    def __init__(self, model: Model):
        """Takes only Modl as input and extract data to attributes."""
        self.input_path = os.path.join(model.model_path, "Output")
        self.output_path = model.output_path
        self.identifier = model.identifier
        self.spinup_period = model.spinup_period
        self.raw_data: dict[int, pd.DataFrame] = {}
        self.processed_data: pd.DataFrame = pd.DataFrame()

    def load_data(self):
        """Load all appropriate output files and save to dictionary."""
        self.raw_data = {}
        for path in os.listdir(self.input_path):
            if "Q3K3S3" not in path:
                continue
            # Extract only the filename from the path
            key_name = path.split("_")[-1][:-4]
            # Extract only the digits from the filename (without regex)
            key_name = int("".join([d for d in key_name if d.isdigit()]))
            self.raw_data[key_name] = pd.read_csv(
                os.path.join(self.input_path, path), sep=r'\s+'
            )

    def process_data(self):
        """
        Process raw data from dictionary format into single dataframe.
        I think I have done this in a very inefficient way but it works.
        """
        tidy_dfs = []
        for key, value in self.raw_data.items():
            start_date = pd.Timestamp(
                year=value.Year.iloc[0],
                month=value.Month.iloc[0],
                day=value.Day.iloc[0]
            )
            end_date = pd.Timestamp(
                year=value.Year.iloc[-1],
                month=value.Month.iloc[-1],
                day=value.Day.iloc[-1]
            )
            value.index = pd.date_range(start=start_date, end=end_date)
            value = value[['GWL(m)']]
            value.columns = [key]
            tidy_dfs.append(value)
        df = pd.concat(tidy_dfs, axis=1).sort_index()
        # Add ID as an index column at level=0
        df = pd.concat([df], keys=[self.identifier], names=['ID'])
        df.index = df.index.rename('date', level=1)
        # Add spinup or forecast labels to output
        df['period'] = "spinup"
        df.iloc[self.spinup_period:, df.columns.get_loc('period')] = "forecast"
        df = df.set_index('period', drop=True, append=True)
        df = df.reorder_levels(['ID', 'period', 'date'])
        df = df.sort_index(axis=1)
        self.processed_data = df

    def write_file(self):
        """Write out tidy data to file."""
        self.processed_data.to_csv(
            os.path.join(self.output_path, self.identifier + '.csv')
        )
