from unittest import TestCase

from person.person import Person
from project.project import MAX_AVAILABLE_VOTES, Project


class TestPerson(TestCase):
    person = None
    target = None

    def setUp(self):
        super().setUp()
        # Each time we run a test, create a new person and target to make sure they are at their default values
        # (i.e. no votes cast)
        self.person = Person("Sam")
        self.target = Person("Davy")

    def test_get_remaining_votes(self):
        # No votes assigned, has MAX_AVAILABLE_VOTES still
        self.assertEqual(MAX_AVAILABLE_VOTES, self.person.get_remaining_votes())

    def test_assign_updates_remaining_votes(self):
        # Assign 50 votes and make sure 50 goes away
        self.person.assign_votes(self.target, 50)
        self.assertEqual(MAX_AVAILABLE_VOTES - 50, self.person.get_remaining_votes())

    def test_assign_again_updates_remaining_votes(self):
        # Updating the assigned votes from 50 to 100 should only take away an additional 50 points
        self.person.assign_votes(self.target, 100)
        self.assertEqual(MAX_AVAILABLE_VOTES - 100, self.person.get_remaining_votes())

    def test_assign_max_points_consumes_all_points(self):
        # Assign MAX_AVAILABLE_VOTES to the same person
        self.person.assign_votes(self.target, MAX_AVAILABLE_VOTES)
        self.assertEqual(0, self.person.get_remaining_votes())

    def test_assign_more_votes_than_available_raises_exception(self):
        # If we assign MAX_AVAILABLE_VOTES + 1, it raises an exception
        with self.assertRaises(ValueError):
            self.person.assign_votes(self.target, MAX_AVAILABLE_VOTES + 1)

    def test_assign_no_points_correctly_removes_votes(self):
        # If we assign 0 votes, it returns back to MAX_AVAILABLE_VOTES
        self.person.assign_votes(self.target, 0)
        self.assertEqual(MAX_AVAILABLE_VOTES, self.person.get_remaining_votes())

    def test_assign_negative_points_throws_exception(self):
        with self.assertRaises(ValueError):
            self.person.assign_votes(self.target, -1)

    def test_get_total_score(self):
        # Following data is from page 10 of the worked example in the brief
        xiang = Person("Xiang")
        bogdan = Person("Bogdan")
        asim = Person("Asim")

        xiang.assign_votes(bogdan, 50)
        xiang.assign_votes(asim, 50)

        bogdan.assign_votes(xiang, 35)
        bogdan.assign_votes(asim, 65)

        asim.assign_votes(xiang, 40)
        asim.assign_votes(bogdan, 60)

        project = Project("test_get_total_score_project", [xiang, bogdan, asim])

        self.assertEqual(23, xiang.get_total_score(project))
        self.assertEqual(38, bogdan.get_total_score(project))
        self.assertEqual(39, asim.get_total_score(project))
