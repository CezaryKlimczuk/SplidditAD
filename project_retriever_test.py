import builtins
from contextlib import contextmanager
from unittest import TestCase
from unittest.mock import Mock

from project import Project, Person
from project_repository import ProjectRepository
from project_retriever import ProjectRetriever


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


project_repo = ProjectRepository()
project_retriever = ProjectRetriever(project_repo)
project_name = "project_1"
members = [Person("Tom"), Person("Steven"), Person("Bob")]
project = Project(project_name, members)


class ProjectRetrieverTest(TestCase):

    def setUp(self):
        super().setUp()
        project_repo.put(project)

    def tearDown(self):
        super().tearDown()
        project_repo.delete_all()

    def test_project_retriever_returns_project_for_valid_input(self):
        with mock_inputs([project_name]):
            retrieved_project = project_retriever.get_project_from_user()
            self.assertEqual(project, retrieved_project)

    def test_project_retriever_asks_for_input_again_if_project_cant_be_found(self):
        project_names = ["1", "2", "3", project_name]

        with mock_inputs(project_names):
            retrieved_project = project_retriever.get_project_from_user()
            self.assertEqual(retrieved_project, project)
