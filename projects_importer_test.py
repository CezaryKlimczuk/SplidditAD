from unittest import TestCase

from project import Project, Person
from project_repository import ProjectRepository
from projects_importer import ProjectsImporter

valid_projects = "projects_valid_test.csv"
repo = ProjectRepository()


class TestProjectsImporter(TestCase):

    def setUp(self):
        super().setUp()
        repo.delete_all()

    def tearDown(self):
        super().tearDown()
        repo.delete_all()

    def test_file_not_found(self):
        # Create an importer with a file that doesn't exist
        no_file_importer = ProjectsImporter("nonexistantfile.csv", repo)

        # Attempting to import the projects if the file doesn't exist shouldn't raise an exception
        no_file_importer.import_projects()

        # It should instead import nothing
        self.assertEqual(set(), repo.get_all())

    def test_import_valid_projects(self):
        self.assertEqual(set(), repo.get_all())
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
        asim.votes[bogdan] = 60
        asim.votes[xiang] = 40
        bogdan.votes[xiang] = 35
        bogdan.votes[asim] = 65
        xiang.votes[bogdan] = 50
        xiang.votes[asim] = 50

        name = "C1-ENGS101P"
        C1_ENGS101P = Project(name, [asim, bogdan, xiang])

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
        axel.votes[bo] = 50
        axel.votes[chuzi] = 50
        bo.votes[chuzi] = 60
        bo.votes[axel] = 40
        chuzi.votes[bo] = 65
        chuzi.votes[axel] = 45

        name = "ProjectC"
        project_C = Project(name, [axel, bo, chuzi])

        # ===============================

        self.assertEqual({C1_ENGS101P, project_C}, repo.get_all())
