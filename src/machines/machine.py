import boto3


class Machine:

    def __init__(self, connector: boto3.session.Session):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        """

        self.__ecs_client = connector.client(service_name='stepfunctions')

    def describe_state_machine(self, machine: dict):
        pass

    def create_state_machine(self, machine: dict):
        pass

    def delete_state_machine(self, machine: dict):
        pass
