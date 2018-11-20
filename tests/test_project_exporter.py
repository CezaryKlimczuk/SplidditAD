import os
from unittest import TestCase

from csv.projects_exporter import ProjectsExporter
from project.project_repository import ProjectRepository
from tests import test_helper
from tests.data_sources import data_sources

repo = ProjectRepository()
file_name = data_sources.exported_projects
exporter = ProjectsExporter(file_name, repo)


def delete_target_export_file():
    if os.path.exists(file_name):
        os.remove(file_name)


class TestProjectsExporter(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        delete_target_export_file()

    def test_file_created_when_not_exists(self):
        self.assert_file_exists(False)

        # Add a project to the repo
        project = test_helper.create_project("project_1", ["a", "b", "c"])
        repo.put(project)

        # Export all projects
        exporter.export_projects()

        # Make sure the file was created
        self.assert_file_exists()

    def test_export_projects(self):
        # self.fail()
        pass

    def assert_file_exists(self, exists=True):
        self.assertEquals(exists, os.path.isfile(file_name))
