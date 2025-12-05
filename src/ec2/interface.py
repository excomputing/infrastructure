"""Module interface.py"""
import logging

import boto3

import src.ec2.settings
import src.ec2.template
import src.elements.s3_parameters as s3p


class Interface:
    """
    Amazon Elastic Compute Cloud (Amazon EC2)
    """

    def __init__(self, connector: boto3.session.Session, s3_parameters: s3p.S3Parameters, arguments: dict):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        :param arguments:
        """

        self.__connector = connector
        self.__s3_parameters = s3_parameters
        self.__arguments = arguments

        # Temporary set-up.  In future the raw `specifications` & `data` will be read from files.
        self.__settings = src.ec2.settings.Settings(connector=self.__connector, arguments=self.__arguments)

    def exc(self):
        """

        :return:
        """

        template = src.ec2.template.Template(connector=self.__connector)
        logging.info(self.__settings.specifications())
        logging.info(self.__settings.data())

        template.exc(specifications=self.__settings.specifications(), data=self.__settings.data())
