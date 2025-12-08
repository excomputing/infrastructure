"""Module settings.py"""
import os

import src.elements.ec2_pathways as ec2p
import src.functions.objects


class Settings:
    """
    Reads-in the Base 64 computing details file.
    """

    def __init__(self, ec2_pathways: ec2p.EC2Pathways):
        """
        Constructor
        """

        self.__ec2_pathways = ec2_pathways

        # Root
        self.__path = os.path.join(os.getcwd(), 'src')

        # The network interfaces data of the launch template data section
        self.network_interfaces = [
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

    def template(self):
        """
        e.g., ['...', 'template.json']

        :return:
        """

        objects = src.functions.objects.Objects()

        return objects.read(uri=os.path.join(self.__path, *self.__ec2_pathways.template))

    def directives(self) -> str:
        """
        e.g., ['...', 'directives-base64.txt']

        :return:
        """

        with open(file=os.path.join(self.__path, *self.__ec2_pathways.directives), mode='r') as disk:
            encodings = disk.read()

        return encodings
