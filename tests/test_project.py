from unittest import TestCase

from tests import test_helper

PROJECT_NAME = "project_name"
PROJECT_MEMBER_NAMES = ["aaa", "bb", "cc", "dd"]

project = test_helper.create_project(PROJECT_NAME, PROJECT_MEMBER_NAMES)


class TestProject(TestCase):

    def test_get_member_count(self):
        self.assertEqual(4, project.get_member_count())

    def test_get_longest_member(self):
        self.assertEqual("aaa", project.get_longest_member().name)

    def test_show_details(self):
        # TODO
        pass

    def test_raises_exception_for_short_name(self):
        with self.assertRaises(ValueError):
            test_helper.create_project("  ", ["aa", "bb", "cc"])

    def test_raises_exception_for_invalid_char_in_name(self):
        members = ["aa", "bb", "cc"]

        with self.assertRaises(ValueError):
            test_helper.create_project("invalid.project.name", members)

        with self.assertRaises(ValueError):
            test_helper.create_project("new\nline\nin\nmiddle", members)

    def test_raises_exception_for_duplicate_members(self):
        with self.assertRaises(ValueError):
            test_helper.create_project("duplicate_members", ["aa", "aa", "cc"])

    def test_not_enough_members_raises_exception(self):
        with self.assertRaises(ValueError):
            test_helper.create_project("not enough members", ["aa", "bb"])

    def test_eq_members_in_different_order(self):
        # Same project but with members order reversed
        members = list(reversed(PROJECT_MEMBER_NAMES))
        project_reversed_members = test_helper.create_project(PROJECT_NAME, members)
        self.assertEqual(project, project_reversed_members)

    def test_eq_fewer_members(self):
        # Same project name but fewer members
        fewer_members = PROJECT_MEMBER_NAMES.copy()
        fewer_members.remove("dd")
        project_fewer_members = test_helper.create_project(PROJECT_NAME, fewer_members)
        self.assertNotEqual(project, project_fewer_members)

    def test_eq_more_members(self):
        # Same project name and has the same members + additional members
        project_more_members = test_helper.create_project(PROJECT_NAME, PROJECT_MEMBER_NAMES + ["ee"])
        self.assertNotEqual(project, project_more_members)

    def test_eq_diff_member_names(self):
        # Same project name but all members have a different name
        diff_member_names = list(map(lambda name: name + "_diff", PROJECT_MEMBER_NAMES))
        project_with_diff_member_names = test_helper.create_project(PROJECT_NAME, diff_member_names)
        self.assertNotEqual(project, project_with_diff_member_names)

    def test_eq_diff_names(self):
        # Different project name and all members have the same name
        project_with_diff_name = test_helper.create_project(PROJECT_NAME + "_1", PROJECT_MEMBER_NAMES)
        self.assertNotEqual(project, project_with_diff_name)

    def test_eq_same_args(self):
        # Has exactly the same arguments passed to it
        project_copy = test_helper.create_project(PROJECT_NAME, PROJECT_MEMBER_NAMES)
        self.assertEqual(project, project_copy)
