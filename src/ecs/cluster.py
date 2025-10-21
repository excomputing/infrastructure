"""Module cluster.py"""
import logging

import boto3


class Cluster:
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html
    """

    def __init__(self, connector: boto3.session.Session):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        """

        self.__ecs_client = connector.client(service_name='ecs')

        # Logging
        logging.basicConfig(level=logging.INFO, format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __inspect(self, definitions: dict):
        """

        :param definitions:
        :return:
        """

        try:
            response = self.__ecs_client.describe_clusters(clusters=[definitions.get('clusterName')])
        except self.__ecs_client.exceptions.ClientException as err:
            raise err from err

        return response

    def __create(self, definitions: dict):
        """

        :param definitions:
        :return:
        """

        message = self.__ecs_client.create_cluster(
            clusterName = definitions.get('clusterName'),
            tags=definitions.get('tags')            )
        self.__logger.info('Created Cluster: %s', message['cluster']['clusterName'])

    def create_cluster(self, definitions: dict):
        """

        :param definitions:
        :return:
        """

        response = self.__inspect(definitions=definitions)

        if not response['clusters']:
            self.__create(definitions=definitions)
            return None

        if (response['clusters']) & (response['clusters'][0]['status'] == 'INACTIVE'):
            self.__create(definitions=definitions)
            return None

        if (response['clusters']) & (response['clusters'][0]['status'] == 'ACTIVE'):
            self.__logger.info('%s exists.', definitions.get('clusterName'))
            return None

    def delete_cluster(self, definitions: dict):
        """

        :param definitions:
        :return:
        """

        response = self.__inspect(definitions=definitions)

        if not response['clusters']:
            self.__logger.info('%s does not exist.', definitions.get('clusterName'))
            return None

        message = self.__ecs_client.delete_cluster(
            cluster=definitions.get('clusterName')
        )
        self.__logger.info('Deleted Cluster: %s', message['cluster']['clusterName'])
