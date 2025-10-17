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

    def __inspect(self, definitions: dict) -> list:
        """

        :param definitions:
        :return:
        """

        elements = []
        for status in ['ACTIVE', 'INACTIVE']:
            try:
                response = self.__ecs_client.list_task_definitions(
                    familyPrefix=definitions.get('family'), status=status)
                elements.append(response['taskDefinitionArns'])
            except self.__ecs_client.exceptions.ClientException:
                self.__logger.info('%s does not exist.', definitions.get('family'))
            except botocore.exceptions.ClientError as err:
                raise err from err

        return sum(elements, [])

    def __delete_task_definitions(self, element: str):
        """

        :param element:
        :return:
        """

        try:
            message = self.__ecs_client.delete_task_definitions(
                taskDefinitions=[element]
            )
            self.__logger.info('%s deleted.', message['taskDefinitions'][0]['family'])
        except self.__ecs_client.exceptions.ClientException:
            self.__logger.info('%s does not exist.', element.rsplit(sep='/', maxsplit=1)[1])
        except botocore.exceptions.ClientError as err:
            raise err from err

    def deregister_task_definition(self, definitions: dict):
        """

        :param definitions:
        :return:
        """

        elements = self.__inspect(definitions=definitions)

        # If `elements` is empty, there are no tasks to deregister.
        if not elements:
            self.__logger.info('deregister applicable: false')
            return None

        # Each element is an Amazon Resource Name string, each string includes a task definition family
        # name, and a revision number.
        for element in elements:
            message = self.__ecs_client.deregister_task_definition(
                taskDefinition=element
            )
            self.__delete_task_definitions(element=message['taskDefinition']['taskDefinitionArn'])
