"""Module watch.py"""
import logging

import boto3
import botocore.exceptions


class Watch:
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html
    """

    def __init__(self, connector: boto3.session.Session):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        """

        self.__logs_client = connector.client(service_name='logs')

        # Logging
        logging.basicConfig(level=logging.INFO, format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __inspect(self, definitions: dict) -> dict:

        try:
            response = self.__logs_client.describe_log_groups(
                logGroupNamePattern=definitions.get('logGroupName'),
                logGroupClass=definitions.get('logGroupClass'))
        except botocore.exceptions.ClientError as err:
            raise err from err

        return response

    def create_log_group(self, definitions: dict):
        """

        :param definitions:
        :return:
        """

        response = self.__inspect(definitions=definitions)

        if response['logGroups']:
            self.__logger.info(f'Cloud Watch Log Groups: {definitions.get('logGroupName')} exists')
            return None

        try:
            self.__logs_client.create_log_group(
                logGroupName=definitions.get('logGroupName'),
                tags=definitions.get('tags'),
                logGroupClass=definitions.get('logGroupClass')
            )
        except botocore.exceptions.ClientError as err:
            raise err from err

    def delete_log_group(self, definitions: dict):
        """

        :param definitions:
        :return:
        """

        response = self.__inspect(definitions=definitions)

        if not response['logGroups']:
            self.__logger.info('Cloud Watch Log Groups: %s does not exist.', definitions.get('logGroupName'))
            return None

        try:
            message = self.__logs_client.delete_log_group(
                logGroupName=definitions.get('logGroupName')
            )
            if message:
                self.__logger.info('Deleted log group %s', message['logGroups']['logGroupName'])
        except self.__logs_client.exceptions.ResourceNotFoundException:
            self.__logger.info('Cloud Watch Log Groups: %s does not exist.',
                               definitions.get('logGroupName'))
        except botocore.exceptions.ClientError as err:
            raise err from err
