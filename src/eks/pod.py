"""Module pod.py"""
import json
import logging
import os

import boto3
import botocore.exceptions

import src.functions.objects


class Pod:
    """
    AmazonEKSPodIdentityAmazonCloudWatchObservabilityRole
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/create_role.html
    """

    def __init__(self, connector: boto3.session.Session, arguments: dict):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param arguments:
        """

        self.__connector = connector
        self.__iam_client = self.__connector.client(service_name='iam')
        self.__arguments = arguments

        # Instances
        self.__objects = src.functions.objects.Objects()

    def __get_trust_policy(self) -> str:
        """

        :return:
        """

        objects = self.__objects.read(uri=os.path.join(os.getcwd(), 'src', 'eks', 'pod-trust-policy.json'))

        return json.dumps(objects)

    def __call__(self, max_session_duration: int = 10800):
        """

        :param max_session_duration:
        :return:
        """

        role_name = 'AmazonEKSPodIdentityRole'

        # Create baseline role
        try:
            specification: dict = self.__iam_client.create_role(
                Path='/',
                RoleName=role_name,
                AssumeRolePolicyDocument=self.__get_trust_policy(),
                Description='EKS Pods Identity Role: Allows pods running in Amazon EKS cluster to access AWS resources.',
                MaxSessionDuration=max_session_duration,
                Tags=[
                    {'Key': 'project', 'Value': self.__arguments.get('project_tag')}
                ]
            )
        except self.__iam_client.exceptions.EntityAlreadyExistsException:
            logging.info('%s exists', role_name)
            return None
        except botocore.exceptions.ClientError as err:
            raise err from err

        logging.info(specification)

        # Attach role policy
        policies = ['CloudWatchAgentServerPolicy', 'CloudWatchNetworkFlowMonitorAgentPublishPolicy',
                    'AmazonEKS_CNI_Policy']

        for policy in policies:
            message = self.__iam_client.attach_role_policy(
                RoleName=specification.get('Role').get('RoleName'),
                PolicyArn=f'arn:aws:iam::aws:policy/{policy}')
            logging.info(message)

        # Service role policy
        message = self.__iam_client.attach_role_policy(
            RoleName=specification.get('Role').get('RoleName'),
            PolicyArn='arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy')
        logging.info(message)
