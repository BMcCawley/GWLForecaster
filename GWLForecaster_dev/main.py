"""
Perform groundwater level modelling using AquiModAWS.
Uses Input_Form.xlsx as data source and configuration.

Author:
    Brogan McCawley 16/08/2021
"""

from session_resources.input_form import InputForm
from session_resources.session import Session


def main():
    input_form_path = "Input_Form.xlsx"
    input_form = InputForm(input_form_path)
    input_form.check_unique_id()
    session = Session(input_form)
    session.initialise_models()
    session.execute()


if __name__ == '__main__':
    main()
