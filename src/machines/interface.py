
import logging

import boto3

import src.elements.s3_parameters as s3p
import src.functions.secret
import src.s3.configurations


class Interface:

    def __init__(self, connector: boto3.session.Session, s3_parameters: s3p.S3Parameters, arguments: dict):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        :param arguments: A suite of values/arguments vis-à-vis particular to a project
        """

        self.__connector = connector
        self.__s3_parameters = s3_parameters
        self.__arguments = arguments

        # An instance for reading S3 (Simple Storage Service) hosted based configurations
        self.__s3_configurations = src.s3.configurations.Configurations(connector=self.__connector)

        # Secrets
        self.__secrets = self.__get_secrets()

    def __get_secrets(self) -> dict:
        """
        ecs_endpoint = __secrets.get('ecs-endpoint')
        sfn_role_arn = __secrets.get('sfn-role-arn')
        topic_arn = __secrets.get('topic-arn')

        :return:
        """

        secret = src.functions.secret.Secret(connector=self.__connector)
        return secret.exc(secret_id=self.__arguments.get('project_key_name'))

    def __states_computing(self, definition: dict):
        """

        :param definition:
        :return:
        """

        states: dict = definition.get('States')
        keys = [state for state in list(states.keys()) if not state.lower().__contains__('notify')]
        logging.info(keys)

        for key in keys:
            definition['States'][key]['Parameters']['NetworkConfiguration']['AwsvpcConfiguration']['Subnets'] = (
                self.__secrets.get('subnets'))
            definition['States'][key]['Parameters']['NetworkConfiguration']['AwsvpcConfiguration']['SecurityGroups'] = (
                self.__secrets.get('security-groups'))
            definition['States'][key]['Parameters']['Clusters'] = (
                    self.__secrets.get('ecs-endpoint') + definition['States'][key]['Parameters']['Clusters'])
            definition['States'][key]['Parameters']['TaskDefinition'] = (
                    self.__secrets.get('ecs-endpoint') + definition['States'][key]['Parameters']['TaskDefinition'])

    def __states_messaging(self):
        pass

    def exc(self, settings: dict):
        """

        :param settings: In relation to cloud compute
        :return:
        """

        machine: dict
        for machine in settings.get('machines'):

            definition: dict = self.__s3_configurations.objects(
                key_name=f'{self.__arguments.get('machines_prefix')}{machine.get('name')}.json')

            # the computing states
            self.__states_computing(definition=definition)

            # the messaging states

            # the machine
