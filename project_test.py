from unittest import TestCase

from test_helper import create_project

project = create_project("project_1", ["a", "b", "c"])


class TestProject(TestCase):

    def test_get_member_count(self):
        self.assertEqual(3, project.get_member_count())

    def test_get_longest_member(self):
        self.assertTrue(project.get_longest_member() in project.members)

        test_subject = create_project("project_2", ["a", "bb", "c", "d"])
        self.assertEqual("bb", test_subject.get_longest_member().name)

        test_subject = create_project("project_2", ["a", "bb", "c", "ddd"])
        self.assertEqual("ddd", test_subject.get_longest_member().name)

    def test_show_details(self):
        # TODO
        pass

    def test_calculate_shares(self):
        # TODO
        pass
