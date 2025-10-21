
import logging

import boto3
import botocore.exceptions

import config
import src.functions.secret
import src.elements.s3_parameters as s3p


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

        self.__ecs_client = connector.client(service_name='ecs')
        self.__s3_parameters = s3_parameters

        # Configurations
        self.__configurations = config.Config()

        # Secrets
        self.__secret = src.functions.secret.Secret(connector=connector)

    def exc(self, definitions: dict):
        """

        :param definitions:
        :return:
        """

        container_definitions: list[dict] = definitions.get('containerDefinitions')
        for c in container_definitions:
            c['logConfiguration']['options']['awslogs-region'] = self.__s3_parameters.region_name


        try:
            self.__ecs_client.register_task_definition(
                family=definitions.get('family'),
                taskRoleArn=self.__secret.exc(secret_id=self.__configurations.project_key_name, node=''),
                executionRoleArn=self.__secret.exc(secret_id=self.__configurations.project_key_name, node=''),
                networkMode=definitions.get('networkMode'),
                containerDefinitions=container_definitions
            )
        except botocore.exceptions.ClientError as err:
            raise err from err
