"""Module settings.py"""
import logging

import boto3

import src.ec2.details
import src.functions.secret


class Settings:
    """
    A temporary set-up
    """

    def __init__(self, connector: boto3.session.Session, arguments: dict):
        """

        :param connector:
        :param arguments:
        """

        self.__connector = connector
        self.__arguments = arguments

        # Instances
        self.__secret = src.functions.secret.Secret(connector=self.__connector)
        self.__assets: dict = self.__secret.exc(secret_id=self.__arguments.get('project_key_name'))

        # Data
        self.__network_interfaces = [
            {
                "AssociatePublicIpAddress": True,
                "DeleteOnTermination": True,
                "DeviceIndex": 0,
                "Groups": None,
                "InterfaceType": "interface",
                "SubnetId": None,
                "NetworkCardIndex": 0
            }
        ]

        self.__data = {
            "EbsOptimized": True,
            "IamInstanceProfile": {"Arn": None},
            "BlockDeviceMappings": [
                {
                    "DeviceName": "/dev/sda1",
                    "Ebs": {
                        "Encrypted": False,
                        "DeleteOnTermination": True,
                        "Iops": 3000,
                        "VolumeSize": 29,
                        "VolumeType": "gp3",
                        "Throughput": 125
                    }
                }
            ],
            "ImageId": "ami-0f64121fa59598bf7",
            "InstanceType": "t3.small",
            "KeyName": None,
            "Monitoring": {
                "Enabled": False
            },
            "Placement": {
                "AvailabilityZone": None,
                "Tenancy": "default"
            },
            "DisableApiTermination": False,
            "InstanceInitiatedShutdownBehavior": "terminate",
            "UserData": None,
            "TagSpecifications": [
                {
                    "ResourceType": "instance",
                    "Tags": [{"Key": "project", "Value": self.__arguments.get('project_tag')}]
                }
            ],
            "CapacityReservationSpecification": {
                "CapacityReservationPreference": "open"
            },
            "HibernationOptions": {
                "Configured": False
            },
            "MetadataOptions": {
                "HttpTokens": "optional",
                "HttpPutResponseHopLimit": 1,
                "HttpEndpoint": "enabled",
                "HttpProtocolIpv6": "disabled",
                "InstanceMetadataTags": "enabled"
            }
        }

    def specifications(self) -> dict:
        """

        :return:
        """

        return {
            "LaunchTemplateName": "EnvironmentCompute",
            "VersionDescription": "The compute outline of the environment project.",
            "TagSpecifications": [{
                "ResourceType": "launch-template",
                "Tags": [{"Key": "project", "Value": self.__arguments.get('project_tag')}]
            }]
        }

    def data(self) -> dict:
        """

        :return:
        """

        self.__data['IamInstanceProfile']['Arn'] = self.__assets.get('i-am-instance-profile')
        self.__data['KeyName'] = self.__assets.get('key-name')
        self.__data['Placement']['AvailabilityZone'] = self.__assets.get('availability-zone')
        self.__data['UserData'] = src.ec2.details.Details().__call__()

        parts = []
        for part in self.__network_interfaces:
            part['Groups'] = self.__assets.get('security-groups')
            part['SubnetId'] = self.__assets.get('subnet-id')
            parts.append(part)

        self.__data['NetworkInterfaces'] = parts

        return self.__data
