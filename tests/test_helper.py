import builtins
from contextlib import contextmanager
from unittest.mock import Mock

from project import Person, Project


def create_project(project_name, member_names):
    project_members = []
    for name in member_names:
        project_members.append(Person(name))

    return Project(project_name, project_members)


@contextmanager
def mock_inputs(mock_results):
    """
    Mocks the input() fun to return the next element from mock_results each new time it is called.
    If input() is called more times than there are mock results, an exception is raised

    e.g.
    mock_inputs(["1", "2", "3"])

    IN:
    print(input())
    print(input())
    print(input())

    OUT:
    "1"
    "2"
    "3"

    :param mock_results: The results that input() will return in consecutive order
    """
    original_input = builtins.input
    builtins.input = Mock()
    builtins.input.side_effect = mock_results
    yield
    builtins.input = original_input
