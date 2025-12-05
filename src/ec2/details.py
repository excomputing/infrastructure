"""Module details.py"""
import logging
import os


class Details:
    """
    Reads-in the Base 64 computing details file.
    """

    def __init__(self):
        """
        Constructor
        """

        self.__path = os.path.join(os.getcwd(), 'src', 'ec2')

    def __call__(self) -> str:
        """

        :return:
        """


        with open(file=os.path.join(self.__path, 'data-base64.txt'), mode='r') as disk:
            encodings = disk.read()

        logging.info(encodings)

        return encodings
