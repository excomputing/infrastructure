
import logging

import boto3

import config
import src.functions.secret


class Register:
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/register_task_definition.html
    """

    def __init__(self, connector: boto3.session.Session):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        """

        self.__ecs_client = connector.client(service_name='ecs')

        self.__configurations = config.Config()
        self.__secret = src.functions.secret.Secret(connector=connector)

        # Logging
        logging.basicConfig(level=logging.INFO, format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def exc(self, definitions: dict):
        """

        :param definitions:
        :return:
        """

        self.__logger.info(definitions.get('family'))

        '''
        try:
            self.__ecs_client.register_task_definition(
                family=definitions.get('family'),
                taskRoleArn=self.__secret.exc(secret_id=self.__configurations.project_key_name, node=''),
                executionRoleArn=self.__secret.exc(secret_id=self.__configurations.project_key_name, node='')
            )
        except botocore.exceptions.ClientError as err:
            raise err from err
        '''
