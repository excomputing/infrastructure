"""Module interface.py"""
import boto3

import src.ecs.cluster
import src.ecs.watch
import src.elements.s3_parameters as s3p


class Interface:
    """
    The interface to the container service programs
    """

    def __init__(self, connector: boto3.session.Session, s3_parameters: s3p.S3Parameters, arguments: dict, settings: dict):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        :param arguments: A suite of values/arguments vis-à-vis particular to a project
        :param settings: In relation to cloud compute
        """

        self.__connector = connector
        self.__s3_parameters = s3_parameters
        self.__arguments = arguments
        self.__settings = settings

    def exc(self):
        """

        :return:
        """

        # Elastic Container Service Clusters
        __cluster = src.ecs.cluster.Cluster(connector=self.__connector)
        for cluster in self.__settings.get('clusters'):
            definitions = cluster
            __cluster.create_cluster(definitions=definitions)

        # Cloud Watch Log Groups
        __watch = src.ecs.watch.Watch(connector=self.__connector)
        for watch in self.__settings.get('watches'):
            definitions = watch
            definitions['tags']['awslogs-region'] = self.__s3_parameters.region_name
            __watch.create_log_group(definitions=definitions)
