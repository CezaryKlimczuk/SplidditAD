from unittest import TestCase

from project.project_creator import ProjectCreator
from project.project_repository import ProjectRepository
from tests import test_helper
from tests.test_helper import mock_inputs

repo = ProjectRepository()
project_creator = ProjectCreator(repo)


class TestProjectCreator(TestCase):

    def setUp(self):
        super().setUp()
        repo.delete_all()

    def test_create_new_project(self):
        name = "project_name"
        member_count = "3"  # input() returns a string so we must use a string when mocking
        foo = "foo"
        bar = "bar"
        baz = "baz"
        mocked_inputs = [name, member_count, foo, bar, baz]

        with test_helper.mock_inputs(mocked_inputs):
            created_project = project_creator.create_new_project()
            self.assertEqual(name, created_project.name)
            self.assertEqual(int(member_count), created_project.get_member_count())

            member_names = [foo, bar, baz]
            for member in created_project.members:
                self.assertTrue(member.name in member_names)

    def test_create_new_project_duplicate_names(self):
        """
        Test that if we attempt to create a new project with a name that already exists, then it asks again
        """
        # Insert a project
        occupied_name = "project_name"
        repo.put(test_helper.create_project(occupied_name, ["aa", "bb", "cc"]))

        name_attempt_1 = occupied_name
        name_attempt_2 = occupied_name
        name_attempt_3 = occupied_name + "_1"

        member_count = "3"  # input() returns a string so we must use a string when mocking
        foo = "foo"
        bar = "bar"
        baz = "baz"
        mocked_inputs = [name_attempt_1, name_attempt_2, name_attempt_3, member_count, foo, bar, baz]
        with mock_inputs(mocked_inputs):
            project = project_creator.create_new_project()
            self.assertEqual(name_attempt_3, project.name)

    def test_create_new_project_duplicate_members(self):
        name = "project_name"
        member_count = "3"  # input() returns a string so we must use a string when mocking
        foo = "foo"
        bar = "bar"
        baz = "baz"
        mocked_inputs = [name, member_count, foo, foo, foo, bar, baz]  # foo is duplicated 3 times
        with mock_inputs(mocked_inputs):
            project = project_creator.create_new_project()

            member_names = {foo, bar, baz}
            for member in project.members:
                self.assertTrue(member.name in member_names)

    def test_create_invalid_project_member_count(self):
        name = "project_name"
        foo = "foo"
        bar = "bar"
        baz = "baz"

        # should keep asking for member count until 3
        mocked_inputs = [name, "", "-1", "0", "1", "2", "3", foo, bar, baz]

        with mock_inputs(mocked_inputs):
            project = project_creator.create_new_project()
            self.assertEqual(3, project.get_member_count())

            member_names = [foo, bar, baz]
            for member in project.members:
                self.assertTrue(member.name in member_names)

    def test_create_invalid_project_invalid_name(self):
        name = "abc"
        mocked_inputs = []

        # First attempt. Too short name. It will then print an error that ' ab ' is invalid
        mocked_inputs += [" ab ", "3", "foo", "bar", "baz"]

        # Second attempt. Special char in name.
        mocked_inputs += ["special.char", "3", "foo", "bar", "baz"]

        # Final attempt. It's valid
        mocked_inputs += [name, "3", "foo", "bar", "baz"]

        with mock_inputs(mocked_inputs):
            project = project_creator.create_new_project()
            self.assertEqual(project.name, name)
