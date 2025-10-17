"""Module main.py"""
import datetime
import logging
import os
import sys

import boto3


def main():
    """
    Entry Point

    :return:
    """

    logger: logging.Logger = logging.getLogger(__name__)
    logger.info('Starting: %s', datetime.datetime.now().isoformat(timespec='microseconds'))

    # Elastic Container Service Clusters
    __cluster = src.ecs.cluster.Cluster(connector=connector)
    for cluster in settings.get('clusters'):
        definitions = cluster
        __cluster.delete_cluster(definitions=definitions)

    # Cloud Watch Log Groups
    __watch = src.ecs.watch.Watch(connector=connector)
    for watch in settings.get('watches'):
        definitions = watch
        definitions['tags']['awslogs-region'] = s3_parameters.region_name
        __watch.delete_log_group(definitions=definitions)

    # Delete Cache Points
    src.functions.cache.Cache().exc()


# noinspection DuplicatedCode
if __name__ == '__main__':

    # Paths
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Modules
    import src.ecs.cluster
    import src.ecs.watch
    import src.elements.service as sr
    import src.elements.s3_parameters as s3p
    import src.functions.cache
    import src.preface.interface

    connector: boto3.session.Session
    s3_parameters: s3p
    service: sr.Service
    arguments: dict
    settings: dict
    connector, s3_parameters, service, arguments, settings = src.preface.interface.Interface().exc()

    main()
