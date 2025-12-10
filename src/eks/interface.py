"""Module interface.py"""
import logging

import boto3

import src.eks.additions
import src.eks.cluster
import src.eks.node
import src.eks.pod
import src.eks.role


class Interface:
    """
    The interface to the Elastic Kubernetes Service programs.
    """

    def __init__(self, connector: boto3.session.Session, arguments: dict):
        """
        https://docs.aws.amazon.com/eks/latest/userguide/cluster-iam-role.html

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param arguments:
        """

        self.__connector = connector
        self.__arguments = arguments

    def exc(self):
        """

        :return:
        """

        src.eks.role.Role(
            connector=self.__connector, arguments=self.__arguments).__call__()

        src.eks.node.Node(
            connector=self.__connector, arguments=self.__arguments).__call__()

        src.eks.pod.Pod(
            connector=self.__connector, arguments=self.__arguments).__call__()

        cluster_name = src.eks.cluster.Cluster(
            connector=self.__connector, arguments=self.__arguments).__call__()

        src.eks.additions.Additions(
            connector=self.__connector, cluster_name=cluster_name).__call__()
