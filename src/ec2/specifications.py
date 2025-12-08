"""Module specifications.py"""
import os

import src.elements.ec2_pathways as ec2p
import src.functions.objects


class Specifications:
    """

    <b>Notes</b><br>
    ------<br>
    Reads-in the top level EC2 launch template specifications; probably outlined in
    a `specifications.json` data file.<br>
    """

    def __init__(self):
        """
        Constructor
        """

        self.__path = os.path.join(os.getcwd(), 'src')

    def __call__(self, ec2_pathways: ec2p.EC2Pathways):
        """

        :param ec2_pathways:
        :return:
        """

        objects = src.functions.objects.Objects()

        return objects.read(uri=os.path.join(self.__path, *ec2_pathways.specifications))
