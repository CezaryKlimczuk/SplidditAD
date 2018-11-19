from unittest import TestCase

from project.project import Project
from person.person import Person
from project.project_repository import ProjectRepository
from project.project_retriever import ProjectRetriever
from tests.test_helper import mock_inputs

repo = ProjectRepository()
retriever = ProjectRetriever(repo)
project_name = "project_1"
members = [Person("Tom"), Person("Steven"), Person("Bob")]
project = Project(project_name, members)


class ProjectRetrieverTest(TestCase):

    def setUp(self):
        super().setUp()
        repo.put(project)

    def tearDown(self):
        super().tearDown()
        repo.delete_all()

    def test_project_retriever_returns_project_for_valid_input(self):
        with mock_inputs([project_name]):
            retrieved_project = retriever.get_project_from_user()
            self.assertEqual(project, retrieved_project)

    def test_project_retriever_asks_for_input_again_if_project_cant_be_found(self):
        project_names = ["1", "2", "3", project_name]

        with mock_inputs(project_names):
            retrieved_project = retriever.get_project_from_user()
            self.assertEqual(retrieved_project, project)
