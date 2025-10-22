"""Module machine.py"""
import logging

import boto3
import botocore.exceptions


class Machine:
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html
    """

    def __init__(self, connector: boto3.session.Session, secrets: dict):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param secrets:
        """

        self.__sfn_client = connector.client(service_name='stepfunctions')
        self.__secrets = secrets

    def describe_state_machine(self, machine: dict) -> bool:
        """

        :param machine:
        :return:
        """

        try:
            response = self.__sfn_client.describe_state_machine(
                stateMachineArn=self.__secrets.get('sfn-endpoint') + machine.get('name')
            )
            logging.info('The state machine - %s - exists', response['name'])
            return True
        except self.__sfn_client.exceptions.StateMachineDoesNotExist:
            logging.info('The state machine - %s - does not exist', machine.get('name'))
            return False
        except botocore.exceptions.ClientError as err:
            raise err from err

    def update_state_machine(self, machine: dict):
        """

        :param machine:
        :return:
        """

        try:
            response = self.__sfn_client.update_state_machine(
                stateMachineArn=self.__secrets.get('sfn-endpoint') + machine.get('name'),
                definition=machine.get('definition'), roleArn=machine.get('roleArn'),
                loggingConfiguration=machine.get('loggingConfiguration'),
                tracingConfiguration=machine.get('tracingConfiguration'),
                publish=machine.get('publish'), versionDescription=machine.get('versionDescription'))
            logging.info(response['stateMachineVersionArn'].rsplit(sep=':', maxsplit=2)[-2:-1])
        except botocore.exceptions.ClientError as err:
            raise err from err

    def create_state_machine(self, machine: dict):
        """

        :param machine:
        :return:
        """

        exist = self.describe_state_machine(machine=machine)

        # if it exists, update it
        if exist:
            self.update_state_machine(machine=machine)
            return None

        # otherwise, create it
        try:
            response = self.__sfn_client.create_state_machine(
                name=machine.get('name'),
                definition=machine.get('definition'), roleArn=machine.get('roleArn'), type=machine.get('type'),
                loggingConfiguration=machine.get('loggingConfiguration'), tags=machine.get('tags'),
                tracingConfiguration=machine.get('tracingConfiguration'), publish=machine.get('publish'),
                versionDescription=machine.get('versionDescription'))
            logging.info(response['stateMachineArn'].rsplit(sep=':', maxsplit=1)[1])
        except botocore.exceptions.ClientError as err:
            raise err from err

    def delete_state_machine(self, machine: dict):
        """

        :param machine:
        :return:
        """

        exist = self.describe_state_machine(machine=machine)

        # if the state machine in question does not exist
        if not exist:
            logging.info('A state machine named %s does not exist', machine.get('name'))
            return None

        # otherwise, delete it
        try:
            message = self.__sfn_client.delete_state_machine(
                stateMachineArn=self.__secrets.get('sfn-endpoint') + machine.get('name'))
            logging.info('Does the state machine %s still exists: %s', machine.get('name'), bool(message))
        except self.__sfn_client.exceptions.InvalidArn:
            raise 'Invalid Amazon Resource Name'
        except botocore.exceptions.ClientError as err:
            raise err from err
