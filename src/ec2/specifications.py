import os
import src.functions.objects
import src.elements.ec2_pathways as ec2p


class Specifications:

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
