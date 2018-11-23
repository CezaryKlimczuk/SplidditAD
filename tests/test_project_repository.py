from unittest import TestCase

from project.project_repository import ProjectRepository
from tests.test_helper import create_project

repo = ProjectRepository()
project_1 = create_project("project_1", ["aa", "bb", "cc"])
project_2 = create_project("project_2", ["dd", "ee", "ff"])


class TestProjectRepository(TestCase):

    def tearDown(self):
        super().tearDown()
        repo.delete_all()

    def test_put(self):
        self.assert_repo_eq([])

        repo.put(project_1)
        self.assert_repo_eq([project_1])

    def test_put_duplicates(self):
        self.assert_repo_eq([])

        repo.put(project_1)
        repo.put(project_1)
        self.assert_repo_eq([project_1])

    def test_put_list(self):
        self.assert_repo_eq([])

        repo.put([project_1, project_2])
        self.assert_repo_eq([project_1, project_2])

    def test_put_list_with_duplicates(self):
        self.assert_repo_eq([])

        repo.put([project_1, project_2, project_2])
        self.assert_repo_eq([project_1, project_2])

    def test_put_same_name(self):
        repo.put(project_1)
        self.assert_repo_eq([project_1])

        # Check that if we attempt to put a project with the same name then it replaces the project with that name
        project_with_same_name = create_project(project_1.name, ["dd", "ee", "ff"])
        repo.put(project_with_same_name)
        self.assert_repo_eq([project_with_same_name])

    def test_delete(self):
        self.assert_repo_eq([])

        repo.put(project_1)
        self.assert_repo_eq([project_1])

        repo.delete(project_1)
        self.assert_repo_eq([])

    def test_delete_all(self):
        self.assert_repo_eq([])

        repo.put(project_1)
        repo.put(project_2)
        self.assert_repo_eq([project_1, project_2])

        repo.delete_all()
        self.assert_repo_eq([])

    def test_get_all(self):
        self.assert_repo_eq([])

        repo.put(project_1)
        self.assert_repo_eq([project_1])

        repo.put(project_2)
        self.assert_repo_eq([project_1, project_2])

    def test_find_by_name(self):
        self.assert_repo_eq([])

        self.assertIsNone(repo.find_by_name(project_1.name))

        repo.put(project_1)
        self.assertEqual(project_1, repo.find_by_name(project_1.name))

        repo.put(project_2)
        self.assertEqual(project_2, repo.find_by_name(project_2.name))

    def assert_repo_eq(self, values):
        self.assertEqual(set(values), repo.get_all())
