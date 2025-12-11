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

    # Delete State Machines
    __machine = src.machines.machine.Machine(connector=connector, secrets=secrets)
    for machine in settings.get('machines'):
        __machine.delete_state_machine(machine=machine)

    # Elastic Container Service Tasks
    __task = src.ecs.task.Task(connector=connector, s3_parameters=s3_parameters)
    for task in settings.get('tasks'):
        definitions = task
        __task.deregister_task_definition(definitions=definitions)

    # Cloud Watch Log Groups
    __watch = src.ecs.watch.Watch(connector=connector)
    for watch in settings.get('watches'):
        definitions = watch
        definitions['tags']['awslogs-region'] = s3_parameters.region_name
        __watch.delete_log_group(definitions=definitions)

    # Elastic Container Service Clusters
    __cluster = src.ecs.cluster.Cluster(connector=connector)
    for cluster in settings.get('clusters'):
        definitions = cluster
        __cluster.delete_cluster(definitions=definitions)

    # Delete Cache Points
    src.functions.cache.Cache().exc()



if __name__ == '__main__':

    # Paths
    # noinspection DuplicatedCode
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Modules
    import src.ecs.cluster
    import src.ecs.task
    import src.ecs.watch
    import src.elements.service as sr
    import src.elements.s3_parameters as s3p
    import src.functions.cache
    import src.functions.secret
    import src.machines.machine
    import src.preface.interface

    connector: boto3.session.Session
    s3_parameters: s3p
    service: sr.Service
    arguments: dict
    settings: dict
    connector, s3_parameters, service, arguments, settings = src.preface.interface.Interface().exc()

    # Secrets
    __secret = src.functions.secret.Secret(connector=connector)
    secrets = __secret.exc(secret_id=arguments.get('project_key_name'))

    main()
