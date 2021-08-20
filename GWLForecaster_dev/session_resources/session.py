"""
Class Session represents a GWLF modelling session.

Author:
    Brogan McCawley 16/08/2021
"""

import os
from .input_form import InputForm
from .model_resources.model import Model
from .model_resources.input_data import InputData
from .model_resources.observations_txt import ObservationsTxt
from .model_resources.input_txt import InputTxt
from .model_resources.executor import Executor
from .model_resources.output_data import OutputData


class Session:
    """
    Represent a GWLF modelling session. Session implements the package
    model_resources, instantiating models and iteratively executing the
    modelling.
    """
    def __init__(self, input_form: InputForm):
        """
        Initialise Session with input_form.

        Parameter input_form must be a pd.DataFrame with column names of:
            'ID', 'Catchment', 'Spinup Init GWL', 'Forecast Init GWL',
            'Number of Runs'.
        """
        self.input_form = input_form
        self.models: list[Model] = []
        self.models_dir = 'models'  # directory relative to main.py
        self.output_dir = 'output'  # directory relative to main.py

    def initialise_models(self):
        """
        Initialise Model objects and save as list in self.models attribute.
        """
        self.models = [
            Model(
                model_path=os.path.join(self.models_dir, row['Catchment']),
                input_form_path=self.input_form.filepath,
                output_path=self.output_dir,
                identifier=row['ID'],
                catchment=row['Catchment'],
                spinup_init_GWL=row['Spinup Init GWL'],
                forecast_init_GWL=row['Forecast Init GWL'],
                num_runs=row['Number of Runs'])
            for index, row in self.input_form.data.iterrows()]

    def execute(self):
        """
        Execute all models in their entirety, one after the other.
        Models are not executed together, because if the same catchment is
        executed more than once, then output files will become overwritten.

        Objects only take the Model object as an argument during instantiation.
        This shows the utility of Model object being a data class rather
        than performing any behaviour.
        """
        for model in self.models:
            input_data = InputData(model)  # instantiation
            input_data.parse_spinup_data()
            input_data.parse_forecast_data()
            observations_file = ObservationsTxt(model)  # instantiation
            observations_file.process_data()
            observations_file.write_file()
            input_file = InputTxt(model)  # instantiation
            input_file.edit_file()
            executor = Executor(model)  # instantiation
            executor.clear_output_directory()
            executor.execute()
            output_data = OutputData(model)  # instantiation
            output_data.load_data()
            output_data.process_data()
            output_data.write_file()
