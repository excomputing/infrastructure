"""Module register.py"""
import logging
import boto3
import botocore.exceptions

import config
import src.elements.s3_parameters as s3p
import src.functions.secret


class Register:
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/client/register_task_definition.html
    """

    def __init__(self, connector: boto3.session.Session, s3_parameters: s3p.S3Parameters):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        """

        self.__connector = connector
        self.__ecs_client = self.__connector.client(service_name='ecs')
        self.__s3_parameters = s3_parameters

        # Configurations
        self.__configurations = config.Config()
        self.__project_key_name = self.__configurations.project_key_name

        # Secrets
        self.__ecr_endpoint, self.__task_role_arn, self.__execution_role_arn = self.__assets()

    def __assets(self):
        """

        :return:
        """

        secret = src.functions.secret.Secret(connector=self.__connector)

        ecr_endpoint: str = secret.exc(secret_id=self.__project_key_name, node='ecr-endpoint')
        task_role_arn: str = secret.exc(secret_id=self.__project_key_name, node='ecs-role-arn-task')
        execution_role_arn: str = secret.exc(secret_id=self.__project_key_name, node='ecs-role-arn-execution')

        return ecr_endpoint, task_role_arn, execution_role_arn

    def exc(self, definitions: dict):
        """

        :param definitions:
        :return:
        """

        container_definitions: list[dict] = definitions.get('containerDefinitions')

        for c in container_definitions:
            c['logConfiguration']['options']['awslogs-region'] = self.__s3_parameters.region_name
            c['image'] = self.__ecr_endpoint + c['image']

        # Hence
        try:
            message = self.__ecs_client.register_task_definition(
                family=definitions.get('family'),
                taskRoleArn=self.__task_role_arn,
                executionRoleArn=self.__execution_role_arn,
                networkMode=definitions.get('networkMode'),
                containerDefinitions=container_definitions,
                requiresCompatibilities=definitions.get('requiresCompatibilities'),
                cpu=definitions.get('cpu'),
                memory=definitions.get('memory'),
                tags=definitions.get('tags'),
                runtimePlatform=definitions.get('runtimePlatform'))
        except botocore.exceptions.ClientError as err:
            raise err from err

        name = message['taskDefinition']['taskDefinitionArn'].rsplit(sep='/', maxsplit=1)[1]
        logging.info('Created Task Definition: %s', name)
