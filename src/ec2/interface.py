"""Module interface.py"""
import logging

import boto3

import src.ec2.data
import src.ec2.specifications
import src.ec2.template
import src.elements.ec2_pathways as ec2p
import src.elements.s3_parameters as s3p


class Interface:
    """
    Amazon Elastic Compute Cloud (Amazon EC2)
    """

    def __init__(self, connector: boto3.session.Session, s3_parameters: s3p.S3Parameters, arguments: dict):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        :param arguments:
        """

        self.__connector = connector
        self.__s3_parameters = s3_parameters
        self.__arguments = arguments

    def exc(self, ec2_pathways: ec2p.EC2Pathways):
        """

        :return:
        """

        # Specifications
        __specifications = src.ec2.specifications.Specifications()

        # Data
        __data = src.ec2.data.Data(connector=self.__connector, arguments=self.__arguments)

        # Template
        template = src.ec2.template.Template(connector=self.__connector)
        template.exc(specifications=__specifications.__call__(ec2_pathways=ec2_pathways),
                     data=__data.__call__(ec2_pathways=ec2_pathways))
