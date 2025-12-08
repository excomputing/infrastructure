"""Module settings.py"""
import logging

import boto3

import src.ec2.settings
import src.elements.ec2_pathways as ec2p
import src.functions.secret


class Data:
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


    def __call__(self, ec2_pathways: ec2p.EC2Pathways) -> dict:
        """

        :param ec2_pathways:
        :return:
        """

        __settings = src.ec2.settings.Settings(ec2_pathways=ec2_pathways)

        __data = __settings.template()
        __data['IamInstanceProfile'] = {"Arn": self.__assets.get('i-am-instance-profile')}
        __data['KeyName'] = self.__assets.get('key-name')
        __data['Placement']['AvailabilityZone'] = self.__assets.get('availability-zone')
        __data['UserData'] = __settings.directives()

        parts = []
        for part in __settings.network_interfaces:
            part['Groups'] = self.__assets.get('security-groups')
            part['SubnetId'] = self.__assets.get('subnet-id')
            parts.append(part)

        __data['NetworkInterfaces'] = parts

        return __data
