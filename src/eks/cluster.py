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
    def __get_settings() -> dict:
        """

        :return:
        """

        objects = src.functions.objects.Objects()
        settings = objects.read(uri=os.path.join(os.getcwd(), 'src', 'eks', 'settings.json'))
        logging.info(settings)

        return settings

    def __call__(self):
        """
        cluster, additions

        :return:
        """

        try:
            specifications: dict = self.__eks_client.create_cluster(
                name="",
                version="1.34",
                roleArn="",
                resourcesVpcConfig={},
                kubernetesNetworkConfig={},
                logging={},
                tags={"project": self.__arguments.get("project-tag")},
                upgradePolicy={},
                zonalShiftConfig={},
                computeConfig={},
                storageConfig={},
                deletionProtection=False,
                controlPlaneScalingConfig={'tier': 'tier-xl'}
            )
        except botocore.exceptions.ClientError as err:
            raise err from err

        logging.info(specifications)
