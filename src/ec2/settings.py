"""Module details.py"""
import os

import src.functions.objects


class Settings:
    """
    Reads-in the Base 64 computing details file.
    """

    def __init__(self):
        """
        Constructor
        """

        self.__path = os.path.join(os.getcwd(), 'src')

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

    def template(self, strings: list):
        """

        :param strings: e.g., ['eks', 'data.json']
        :return:
        """

        objects = src.functions.objects.Objects()

        return objects.read(uri=os.path.join(self.__path, *strings))

    def directives(self, strings: list) -> str:
        """

        :param strings: e.g., ['eks', 'data-base64.txt']
        :return:
        """

        with open(file=os.path.join(self.__path, *strings), mode='r') as disk:
            encodings = disk.read()

        return encodings
