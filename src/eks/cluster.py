"""Module cluster.py"""
import logging
import os

import boto3
import botocore.exceptions

import src.functions.objects


class Cluster:
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/client/create_cluster.html
    """

    def __init__(self, connector: boto3.session.Session, arguments: dict):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param arguments:
        """

        self.__connector = connector
        self.__eks_client = self.__connector.client(service_name='eks')
        self.__arguments = arguments

    @staticmethod
    def __get_settings_cluster() -> dict:
        """
        Reference: <a
        href="https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/client/create_cluster.html">
        create_cluster</a><br><br>

        :return:
        """

        objects = src.functions.objects.Objects()
        settings = objects.read(
            uri=os.path.join(os.getcwd(), 'src', 'eks', 'cluster.json'))

        return settings

    def __call__(self) -> str:
        """
        cluster, additions

        :return:
        """

        settings: dict = self.__get_settings_cluster()

        try:
            specifications: dict = self.__eks_client.create_cluster(
                name=settings.get('name'),
                version=settings.get('version'),
                roleArn=settings.get('roleArn'),
                resourcesVpcConfig=settings.get('resourcesVpcConfig'),
                kubernetesNetworkConfig=settings.get('kubernetesNetworkConfig'),
                logging=settings.get('logging'),
                tags={"project": self.__arguments.get("project-tag")},
                upgradePolicy=settings.get('upgradePolicy'),
                zonalShiftConfig=settings.get('zonalShiftConfig'),
                computeConfig=settings.get('computeConfig'),
                storageConfig=settings.get('storageConfig'),
                deletionProtection=False,
                controlPlaneScalingConfig=settings.get('controlPlaneScalingConfig')
            )
        except botocore.exceptions.ClientError as err:
            raise err from err

        logging.info(specifications)

        return settings.get("name")
