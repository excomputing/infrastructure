"""Module interface.py"""
import typing

import boto3

import config
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.functions.cache
import src.functions.service
import src.preface.setup
import src.s3.configurations
import src.s3.s3_parameters


class Interface:
    """
    Interface
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

    @staticmethod
    def __get_elements(connector: boto3.session.Session, key_name: str) -> dict:
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param key_name: Of a configurations file
        :return:
        """

        return src.s3.configurations.Configurations(
            connector=connector).objects(key_name=key_name)

    def exc(self) -> typing.Tuple[boto3.session.Session, s3p.S3Parameters, sr.Service, dict, dict]:
        """

        :return:
        """

        connector = boto3.session.Session()

        # Arguments, Settings
        arguments: dict = self.__get_elements(connector=connector, key_name=self.__configurations.argument_key)
        settings: dict = self.__get_elements(connector=connector, key_name=self.__configurations.settings_key)

        # Interaction Instances: Amazon
        s3_parameters: s3p.S3Parameters = src.s3.s3_parameters.S3Parameters(connector=connector).exc()
        service: sr.Service = src.functions.service.Service(
            connector=connector, region_name=s3_parameters.region_name).exc()

        src.preface.setup.Setup().exc()

        return connector, s3_parameters, service, arguments, settings
