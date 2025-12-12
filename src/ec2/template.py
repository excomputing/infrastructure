"""Module template.py"""
import logging

import boto3
import botocore.exceptions


class Template:
    """
    <a
    href="https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_launch_template.html#">
    create_launch_template</a>, <a href="https://docs.aws.amazon.com/AWSEC2/latest/APIReference/errors-overview.html">
    error exceptions</a>
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
        Later: If the template exists, create a new version.

        :param specifications:
        :param data:
        :return:
        """

        try:
            message = self.__ec2_client.create_launch_template(
                LaunchTemplateName=specifications.get('LaunchTemplateName'),
                VersionDescription=specifications.get('VersionDescription'),
                LaunchTemplateData=data,
                TagSpecifications=specifications.get('TagSpecifications')
            )
            logging.info(message)
        except self.__ec2_client.exceptions.InvalidLaunchTemplateName.AlreadyExistsException:
            logging.info('%s exists', specifications.get('LaunchTemplateName'))
        except botocore.exceptions.ClientError as err:
            raise err from err
