import os
from unittest import TestCase

from csv.projects_exporter import ProjectsExporter
from csv.projects_importer import ProjectsImporter
from project.project_repository import ProjectRepository
from tests import test_helper
from tests.data_sources import data_sources

repo = ProjectRepository()
file_name = data_sources.exported_projects
exporter = ProjectsExporter(file_name, repo)
importer = ProjectsImporter(file_name, repo)


class TestProjectsExporter(TestCase):

    def setUp(self):
        super().setUp()
        self.delete_target_export_file()
        repo.delete_all()

    def test_file_created_when_not_exists(self):
        self.assert_file_exists(False)

        # Add a project to the repo
        self.create_project("project_1", 3)

        # Export all projects
        exporter.export_projects()

        # Make sure the file was created
        self.assert_file_exists()

    def test_export_projects(self):
        self.assertEqual(set(), repo.get_all())

        project_1 = self.create_project("project_1", 3)  # Create a project with 3 members
        project_2 = self.create_project("project_2", 5)  # Create a project with 5 members

        exporter.export_projects()

        # The file should always exist upon exporting the projects
        self.assert_file_exists()

        # Purge all the projects from the repo and reimport them to find out if it re-imports them
        repo.delete_all()
        importer.import_projects()

        # Should import the above 2 projects perfectly
        expected = {project_1, project_2}
        actual = repo.get_all()
        self.assertEqual(expected, actual)

    def test_export_incomplete_projects(self):
        project_1 = self.create_project("project_1", 3)  # Create a project with 3 members
        project_2 = self.create_project("project_2", 5)  # Create a project with 5 members

        # incomplete_project is a project where the user hasn't entered the votes.
        # Exporting/importing a project with incomplete votes isn't supported,
        # because we only export/import "valid/completed" projects
        incomplete_project = test_helper.create_project("incomplete_project", ["aa", "bb", "cc"])
        repo.put(incomplete_project)

        # Make sure all valid/invalid projects are in the repo
        self.assertEqual({project_1, project_2, incomplete_project}, repo.get_all())

        exporter.export_projects()
        repo.delete_all()
        importer.import_projects()

        expected = {project_1, project_2}
        actual = repo.get_all()
        self.assertEqual(expected, actual)

    @staticmethod
    def create_project(project_name, member_count):
        """
        Create a project with the given name and member count, and assign votes so that they can be exported.
        The newly created project is put into the repo.

        :param project_name: The name of the project to create
        :param member_count: The number of unique members in the project
        :return: The newly created project
        """
        member_names = []
        for i in range(0, member_count):
            member_name = project_name + "_" + str(i)
            member_names.append(member_name)

        project = test_helper.create_project(project_name, member_names)

        # Assign votes by assigning to each member the remaining votes each member has.
        # That is, each member will assign all their votes to one other person
        for assignor in project.members:
            for assignee in project.members:
                if assignor is not assignee:
                    assignor.assign_votes(assignee, assignor.remaining_votes)

        repo.put(project)
        return project

    def assert_file_exists(self, exists=True):
        self.assertEqual(exists, os.path.isfile(file_name))

    def delete_target_export_file(self):
        if os.path.exists(file_name):
            os.remove(file_name)

        self.assert_file_exists(False)
