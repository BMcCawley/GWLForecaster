"""
Class Model acts as the single interface for exchanging data between the
behavioural/functional classes of GWLF.

Author:
    Brogan McCawley (16/08/2021)
"""

import pandas as pd
from dataclasses import dataclass


@dataclass
class Model:
    """
    Model is the data wrapper for all other classes in the model_resources
    package.
    """
    model_path: str
    input_form_path: str
    output_path: str
    identifier: str
    catchment: str
    spinup_init_GWL: float
    forecast_init_GWL: float
    num_runs: int
    spinup_data: pd.DataFrame = pd.DataFrame()
    forecast_data: pd.DataFrame = pd.DataFrame()
    spinup_period: int = 0
