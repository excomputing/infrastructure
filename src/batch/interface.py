
import subprocess
import logging

import boto3

import src.ec2.interface
import src.elements.s3_parameters as s3p
import src.elements.ec2_pathways as ec2p


class Interface:

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


    def __call__(self):
        """

        :return:
        """

        try:
            page: subprocess.CompletedProcess[bytes] = subprocess.run(
                ["src/batch/machine/directives-base64.sh"], shell=True, check=True)
            logging.info(page.returncode)
        except Exception as err:
            raise err from err

        '''
        ec2_pathways = ec2p.EC2Pathways(
            specifications=['batch', 'machine', 'specifications.json'],
            template=['batch', 'machine', 'template.json'],
            directives=['batch',  'machine', 'directives-base64.txt'])

        src.ec2.interface.Interface(
            connector=self.__connector, s3_parameters=self.__s3_parameters, arguments=self.__arguments).exc(
            ec2_pathways=ec2_pathways)
        '''
