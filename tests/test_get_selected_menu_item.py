import builtins
from contextlib import contextmanager
from unittest import TestCase

import menu
from tests.test_helper import mock_inputs


@contextmanager
def mock_input(mock):
    original_input = builtins.input
    builtins.input = lambda _: mock
    yield
    builtins.input = original_input


def test_get_selected_menu_item(test_case: TestCase, mock_input_val, expected):
    with mock_input(mock_input_val):
        item = menu.get_selected_menu_item()
        test_case.assertEqual(item, expected)


class TestGetSelectedMenuItem(TestCase):

    def test_valid_input(self):
        """
        Tests all possible valid shortcuts
        Tests case sensitivity
        Tests whitespace

        """
        test_get_selected_menu_item(self, "a", menu.about)
        test_get_selected_menu_item(self, "c", menu.create_project)
        test_get_selected_menu_item(self, "v", menu.enter_votes)
        test_get_selected_menu_item(self, "s", menu.show_project)
        test_get_selected_menu_item(self, "q", menu.quit_program)
        test_get_selected_menu_item(self, "C", menu.create_project)
        test_get_selected_menu_item(self, "  C ", menu.create_project)

    def test_invalid_input(self):
        """
        Tests invalid inputs. ("p", "") and completes with valid input "v" (enter votes)
        """
        with mock_inputs(["p", "", "v"]):
            selected = menu.get_selected_menu_item()
            self.assertEqual(menu.enter_votes, selected)
