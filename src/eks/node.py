"""Module node.py"""
import json
import logging
import os

import boto3
import botocore.exceptions

import src.functions.objects


class Node:
    """
    AmazonEKSAutoNodeRole
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/create_role.html
    """

    def __init__(self, connector: boto3.session.Session, arguments: dict, max_session_duration: int = 10800):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param arguments:
        :param max_session_duration:
        """

        self.__connector = connector
        self.__iam_client = self.__connector.client(service_name='iam')
        self.__arguments = arguments
        self.__max_session_duration = max_session_duration

        # Instances
        self.__objects = src.functions.objects.Objects()

    def __get_trust_policy(self) -> str:
        """

        :return:
        """

        objects = self.__objects.read(uri=os.path.join(os.getcwd(), 'src', 'eks', 'node-trust-policy.json'))

        return json.dumps(objects)

    def __set_up(self, role_name: str, policies: list[str]):

        # Create baseline role
        try:
            specification: dict = self.__iam_client.create_role(
                Path='/',
                RoleName=role_name,
                AssumeRolePolicyDocument=self.__get_trust_policy(),
                Description='Allows EKS nodes to connect to EKS Auto Mode clusters and to pull container images from ECR.',
                MaxSessionDuration=self.__max_session_duration,
                Tags=[
                    {'Key': 'project', 'Value': self.__arguments.get('project_tag')}
                ]
            )
        except self.__iam_client.exceptions.EntityAlreadyExistsException:
            logging.info('%s exists', role_name)
            return None
        except botocore.exceptions.ClientError as err:
            raise err from err

        for policy in policies:
            message = self.__iam_client.attach_role_policy(
                RoleName=specification.get('Role').get('RoleName'),
                PolicyArn=f'arn:aws:iam::aws:policy/{policy}'
            )
            logging.info(message)

    def __call__(self):
        """

        :return:
        """

        # Attach roles & policies
        self.__set_up(role_name = 'AmazonEKSAutoNodeRole',
                      policies = ['AmazonEC2ContainerRegistryPullOnly', 'AmazonEKSWorkerNodeMinimalPolicy'])

        self.__set_up(role_name='AmazonEKSNodeRole',
                      policies=['AmazonEKSWorkerNodePolicy', 'AmazonEC2ContainerRegistryReadOnly', 'AmazonEKS_CNI_Policy'])
