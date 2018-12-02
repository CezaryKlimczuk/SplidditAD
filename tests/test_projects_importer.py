import os
from unittest import TestCase

from project.project import Project
from person.person import Person
from project.project_repository import ProjectRepository
from csv.projects_importer import ProjectsImporter
from tests.data_sources.data_sources import no_such_file_projects, invalid_projects, mixed_projects, valid_projects

repo = ProjectRepository()


class TestProjectsImporter(TestCase):

    def setUp(self):
        super().setUp()
        repo.delete_all()

    def tearDown(self):
        super().tearDown()
        repo.delete_all()

    def test_invalid_projects_file_does_not_exist(self):
        # We assume this file doesn't exist in test_file_not_found()
        self.assertFalse(os.path.isfile(no_such_file_projects))

    def test_file_not_found(self):
        # Create an importer with a file that doesn't exist
        no_file_importer = ProjectsImporter(no_such_file_projects, repo)

        # Attempting to import the projects if the file doesn't exist shouldn't raise an exception
        no_file_importer.import_projects()

        # It should instead import nothing
        self.assertEqual(set(), repo.projects)

    def test_import_invalid_projects(self):
        self.assertEqual(set(), repo.projects)
        importer = ProjectsImporter(invalid_projects, repo)
        importer.import_projects()
        # None of the invalid projects should be imported
        # ===========================
        self.assertEqual(set(), repo.projects)

    def test_import_mixed_projects(self):
        self.assertEqual(set(), repo.projects)
        importer = ProjectsImporter(mixed_projects, repo)
        importer.import_projects()
        # Mixed is a concatenation of the invalid and then valid projects
        # The last 2 are the valid ones
        # ===========================
        self.assertEqual(2, len(repo.projects))

    def test_import_valid_projects(self):
        self.assertEqual(set(), repo.projects)
        importer = ProjectsImporter(valid_projects, repo)
        importer.import_projects()

        # ========================
        # C1-ENGS101P,03,
        # Asim,Bogdan,Xiang,
        # Asim,Bogdan,60,Xiang,40,
        # Bogdan,Xiang,35,Asim,65,
        # Xiang,Bogdan,50,Asim,50

        # Members
        asim = Person("Asim")
        bogdan = Person("Bogdan")
        xiang = Person("Xiang")

        # Votes
        asim.assign_votes(bogdan, 60)
        asim.assign_votes(xiang, 40)
        bogdan.assign_votes(xiang, 35)
        bogdan.assign_votes(asim, 65)
        xiang.assign_votes(bogdan, 50)
        xiang.assign_votes(asim, 50)

        name = "C1-ENGS101P"
        c1_engs101p = Project(name, [asim, bogdan, xiang])

        # =========================
        # ProjectC,3,
        # Axel,Bo,Chuzi,
        # Axel,Bo,50,Chuzi,50,
        # Bo,Chuzi,60,Axel,40,
        # Chuzi,Bo,65,Axel,45

        # Members
        axel = Person("Axel")
        bo = Person("Bo")
        chuzi = Person("Chuzi")

        # Votes
        axel.assign_votes(bo, 50)
        axel.assign_votes(chuzi, 50)
        bo.assign_votes(chuzi, 60)
        bo.assign_votes(axel, 40)
        chuzi.assign_votes(bo, 65)
        chuzi.assign_votes(axel, 35)

        name = "ProjectC"
        project_c = Project(name, [axel, bo, chuzi])

        # ===============================

        self.assertEqual({c1_engs101p, project_c}, repo.projects)
