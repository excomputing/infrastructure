"""Module register.py"""
import logging

import boto3


class Template:
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_launch_template.html#
    """

    def __init__(self, connector: boto3.session.Session):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        """

        self.__connector = connector
        self.__ec2_client = self.__connector.client(service_name='ec2')

    def exc(self, specifications: dict, data: dict):
        """

        :param specifications:
        :param data:
        :return:
        """

        message = self.__ec2_client.create_launch_template(
            LaunchTemplateName=specifications.get('LaunchTemplateName'),
            VersionDescription=specifications.get('VersionDescription'),
            LaunchTemplateData=data,
            TagSpecifications=specifications.get('TagSpecifications')
        )

        logging.info(message)
