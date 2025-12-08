import os
import src.functions.objects

class Specifications:

    def __init__(self):
        """
        Constructor
        """

        self.__path = os.path.join(os.getcwd(), 'src')

    def __call__(self, strings: list[str]):
        """

        :param strings:
        :return:
        """

        objects = src.functions.objects.Objects()

        return objects.read(uri=os.path.join(self.__path, *strings))
