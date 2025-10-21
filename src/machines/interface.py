
import boto3
import logging

import config
import src.elements.s3_parameters as s3p
import src.s3.configurations


class Interface:

    def __init__(self, connector: boto3.session.Session, s3_parameters: s3p.S3Parameters, arguments: dict, settings: dict):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        :param arguments: A suite of values/arguments vis-à-vis particular to a project
        :param settings: In relation to cloud compute
        """

        self.__connector = connector
        self.__s3_parameters = s3_parameters
        self.__arguments = arguments
        self.__settings = settings

        self.__machines_prefix = config.Config().machines_prefix
        self.__s3_configurations = src.s3.configurations.Configurations(connector=self.__connector)

    def __definition(self, name: str):

        definition: dict = self.__s3_configurations.objects(key_name=f'{self.__machines_prefix}{name}.json')
        logging.info(definition.get('States'))
        states: dict = definition.get('States')
        logging.info(states.keys())

    def exc(self):

        machine: dict
        for machine in self.__settings.get('machines'):

            self.__definition(name=machine.get('name'))




