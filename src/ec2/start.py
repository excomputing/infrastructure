
import logging

import boto3


class Start:
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

    def exc(self, launch_template: dict):

        self.__ec2_client.run_instances(
            LaunchTemplate=launch_template
        )
