"""config.py"""
import os


class Config:
    """
    Config
    """

    def __init__(self) -> None:
        """
        Constructor<br>
        -----------<br>

        Variables denoting a path - including or excluding a filename - have an underscore suffix; this suffix is
        excluded for names such as warehouse, storage, depository, etc.<br><br>
        """

        # Directories
        self.warehouse: str = os.path.join(os.getcwd(), 'warehouse')

        # Project
        self.project_tag = 'environment'
        self.project_key_name = 'EnvironmentalIntelligence'

        # Keys, etc
        self.s3_parameters_key = 's3_parameters.yaml'
        self.argument_key = 'infrastructure/arguments.json'
        self.settings_key = 'infrastructure/assets/settings.json'
