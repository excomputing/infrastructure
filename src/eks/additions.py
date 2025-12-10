"""Module additions.py"""
import logging
import os

import boto3
import botocore.exceptions

import src.functions.objects


class Additions:
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/client/create_cluster.html
    """

    def __init__(self, connector: boto3.session.Session, cluster_name: str):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param cluster_name:
        """

        self.__connector = connector
        self.__eks_client = self.__connector.client(service_name='eks')
        self.__cluster_name = cluster_name

        # Instances
        self.__objects = src.functions.objects.Objects()

    def __basic(self, addition: dict):
        """

        :param addition:
        :return:
        """

        try:
            specifications = self.__eks_client.create_addon(
                clusterName=self.__cluster_name, addonName=addition.get('addonName'))
        except botocore.exceptions.ClientError as err:
            raise err from err

        logging.info(specifications)

    def __extended(self, addition: dict):
        """

        :param addition:
        :return:
        """

        try:
            specifications = self.__eks_client.create_addon(
                clusterName=self.__cluster_name, addonName=addition.get('addonName'),
                podIdentityAssociations=[
                    {
                        'serviceAccount': addition.get('serviceAccount'), 'roleArn': addition.get('roleArn')
                    },
                ]

            )
        except botocore.exceptions.ClientError as err:
            raise err from err

        logging.info(specifications)

    def __get_settings_additions(self):
        """

        :return:
        """

        settings = self.__objects.read(
            uri=os.path.join(os.getcwd(), 'src', 'eks', 'additions.json'))

        return settings

    def __call__(self):
        """

        :return:
        """

        additions = self.__get_settings_additions()

        for addition in additions:

            if addition.get('extended'):
                self.__extended(addition=addition)
            else:
                self.__basic(addition=addition)
