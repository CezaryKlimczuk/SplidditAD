import math
from unittest import TestCase

from project.project import MAX_AVAILABLE_VOTES
from project.project_voter import ProjectVoter
from tests import test_helper
from tests.test_helper import mock_inputs

project_voter = ProjectVoter()


class TestProjectVoter(TestCase):

    def test_assign_points_from_user(self):
        project = test_helper.create_project("project_name", ["foo", "bar", "baz"])

        # a map where the key is a member name and the value is a map with the target member name as a key and the votes as the value
        votes = {}  # voter -> {voting_on -> vote}

        # foo is assigning points
        foo_bar = str(MAX_AVAILABLE_VOTES)  # foo assigns max to bar
        foo_baz = "0"  # foo assigns 0 to baz
        votes["foo"] = {"bar": MAX_AVAILABLE_VOTES, "baz": 0}

        # bar is assigning points
        bar_foo = str(MAX_AVAILABLE_VOTES - 1)  # bar assigns max but 1 to foo
        bar_baz = "1"  # bar assigns 1 to baz
        votes["bar"] = {"foo": MAX_AVAILABLE_VOTES - 1, "baz": 1}

        # baz is assigning points
        # baz is assigning points to foo
        # baz is stupid
        baz_foo_attempt_1 = str(MAX_AVAILABLE_VOTES + 1)  # baz attempts to assign more points then they have (by 1)
        baz_foo_attempt_2 = str(-1)  # baz attempts to assign negative points...
        baz_foo_attempt_3 = "."  # baz attempts to assign a special character
        baz_foo_attempt_4 = " "  # and some whitespace
        baz_foo_attempt_5 = "2.4"  # and not an integer
        baz_foo_attempt_6 = str(MAX_AVAILABLE_VOTES // 2)  # Finally baz learns and assigns half their points to foo
        # baz is assigning points to bar
        # baz still hasn't got the hang of it...
        baz_bar_attempt_1 = str(math.ceil(MAX_AVAILABLE_VOTES / 2) + 1)  # baz attempts to assign 1 too many points
        baz_bar_attempt_2 = "0"  # they have to assign all their votes so 0 is also incorrect
        baz_bar_attempt_3 = str(math.ceil(MAX_AVAILABLE_VOTES / 2))  # assign the (bigger)  half of their points
        votes["baz"] = {"foo": MAX_AVAILABLE_VOTES // 2, "bar": math.ceil(MAX_AVAILABLE_VOTES / 2)}

        mocked_inputs = (
            # foo is assigning points
            foo_bar,
            foo_baz,

            # bar is assigning points
            bar_foo,
            bar_baz,

            #  baz is assigning points to foo
            baz_foo_attempt_1,
            baz_foo_attempt_2,
            baz_foo_attempt_3,
            baz_foo_attempt_4,
            baz_foo_attempt_5,
            baz_foo_attempt_6,

            # baz is assigning points to bar
            baz_bar_attempt_1,
            baz_bar_attempt_2,
            baz_bar_attempt_3
        )

        with mock_inputs(mocked_inputs):
            project_voter.assign_points_from_user(project)

            for voter in project.members:
                for (voted_on, vote) in voter.votes.items():
                    expected = votes[voter.name][voted_on.name]
                    self.assertEqual(expected, vote)
