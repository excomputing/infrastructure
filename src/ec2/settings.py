"""Module settings.py"""
import logging

import boto3

import src.ec2.details
import src.functions.secret


class Settings:
    """
    A temporary set-up
    """

    def __init__(self, connector: boto3.session.Session, arguments: dict):
        """

        :param connector:
        :param arguments:
        """

        self.__connector = connector
        self.__arguments = arguments

        # Instances
        self.__secret = src.functions.secret.Secret(connector=self.__connector)
        self.__assets: dict = self.__secret.exc(secret_id=self.__arguments.get('project_key_name'))
        self.__details = src.ec2.details.Details()

    def data(self) -> dict:
        """
        Dependencies &Rarr; data.json, data-base64.txt

        :return:
        """

        __data = self.__details.template(strings=['batch', 'data.json'])
        __data['IamInstanceProfile'] = {"Arn": self.__assets.get('i-am-instance-profile')}
        __data['KeyName'] = self.__assets.get('key-name')
        __data['Placement']['AvailabilityZone'] = self.__assets.get('availability-zone')
        __data['UserData'] = self.__details.directives(strings=['batch', 'data-base64.txt'])

        parts = []
        for part in self.__details.network_interfaces:
            part['Groups'] = self.__assets.get('security-groups')
            part['SubnetId'] = self.__assets.get('subnet-id')
            parts.append(part)

        __data['NetworkInterfaces'] = parts

        return __data
