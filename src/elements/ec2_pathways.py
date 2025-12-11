import typing


class EC2Pathways(typing.NamedTuple):
    """
    The data type class ⇾ EC2Pathways

    Attributes
    ----------
    specifications: list[str]
        vis-à-vis launch template
    template: list[str]
        vis-à-vis launch template data
    directives: list[str]
        vis-a-vis launch template data
    """

    specifications: list[str]
    template: list[str]
    directives: list[str]
