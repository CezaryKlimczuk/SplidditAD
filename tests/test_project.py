from unittest import TestCase

from tests import test_helper

PROJECT_NAME = "project_name"
PROJECT_MEMBER_NAMES = ["aa", "b", "c", "d"]

project = test_helper.create_project(PROJECT_NAME, PROJECT_MEMBER_NAMES)


class TestProject(TestCase):

    def test_get_member_count(self):
        self.assertEqual(4, project.get_member_count())

    def test_get_longest_member(self):
        self.assertEqual("aa", project.get_longest_member().name)

    def test_show_details(self):
        # self.fail()
        pass

    def test_raises_exception_for_duplicate_members(self):
        with self.assertRaises(ValueError):
            test_helper.create_project("duplicate_members", ["a", "a", "c"])

    def test_not_enough_members_raises_exception(self):
        with self.assertRaises(ValueError):
            test_helper.create_project("not enough members", ["a", "b"])

    def test_equals(self):
        # Has exactly the same arguments passed to it
        project_copy = test_helper.create_project(PROJECT_NAME, PROJECT_MEMBER_NAMES)
        self.assertEqual(project, project_copy)

        # Different project name and all members have the same name
        project_with_diff_name = test_helper.create_project(PROJECT_NAME + ":1", PROJECT_MEMBER_NAMES)
        self.assertNotEqual(project, project_with_diff_name)

        # Same project name but all members have a different name
        diff_member_names = list(map(lambda name: name + "_diff", PROJECT_MEMBER_NAMES))
        project_with_diff_member_names = test_helper.create_project(PROJECT_NAME, diff_member_names)
        self.assertNotEqual(project, project_with_diff_member_names)

        # Same project name and has the same members + additional members
        project_more_members = test_helper.create_project(PROJECT_NAME, PROJECT_MEMBER_NAMES + ["e"])
        self.assertNotEqual(project, project_more_members)

        # Same project name but fewer members
        fewer_members = PROJECT_MEMBER_NAMES.copy()
        fewer_members.remove("d")
        project_fewer_members = test_helper.create_project(PROJECT_NAME, fewer_members)
        self.assertNotEqual(project, project_fewer_members)

        # Same project but with members order reversed
        members = list(reversed(PROJECT_MEMBER_NAMES))
        print(members)
        project_reversed_members = test_helper.create_project(PROJECT_NAME, members)
        # self.assertEqual(project, project_reversed_members)  # TODO FIX ME!!!! Use a set
