"""Module interface.py"""

import logging

import boto3

import src.eks.role
import src.eks.node
import src.elements.s3_parameters as s3p


class Interface:

    def __init__(self, connector: boto3.session.Session, s3_parameters: s3p.S3Parameters, arguments: dict):
        """
        https://docs.aws.amazon.com/eks/latest/userguide/cluster-iam-role.html

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        :param arguments:
        """

        self.__connector = connector
        self.__s3_parameters = s3_parameters
        self.__arguments = arguments

    def exc(self):
        """

        :return:
        """

        src.eks.role.Role(
            connector=self.__connector, arguments=self.__arguments).__call__()

        src.eks.node.Node(
            connector=self.__connector, arguments=self.__arguments).__call__()
