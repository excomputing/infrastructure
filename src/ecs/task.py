"""Module cluster.py"""
import logging

import boto3
import botocore.exceptions


class Task:
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
        response = self.__ecs_client.describe_task_definition(
                taskDefinition=definitions.get('family')
            )

        :param definitions:
        :return:
        """

        elements = []
        for status in ['ACTIVE', 'INACTIVE']:
            try:
                response = self.__ecs_client.list_task_definitions(
                    familyPrefix=definitions.get('family'),
                    status=status
                )
                self.__logger.info(response)
                elements.append(response['taskDefinitionArns'])
            except self.__ecs_client.exceptions.ClientException:
                self.__logger.info('%s does not exist.', definitions.get('family'))
            except botocore.exceptions.ClientError as err:
                raise err from err

        self.__logger.info('LENGTH: %s', len(elements))

        return sum(elements, [])

    def deregister_task_definition(self, definitions: dict):

        definitions['family'] = 'FewTokens'

        response = self.__inspect(definitions=definitions)
        self.__logger.info(response)

        # `response` will be empty if an active task definition is not found
        if not response:
            self.__logger.info('deregister applicable: false')

    def __delete_task_definitions(self):
        pass
