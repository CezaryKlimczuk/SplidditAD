import builtins
from contextlib import contextmanager
from unittest import TestCase

import menu


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

    def test_get_selected_menu_item(self):
        """
        Tests all possible valid shortcuts
        Tests case sensitivity
        Tests whitespace

        TODO test invalid input
        """
        test_get_selected_menu_item(self, "a", menu.about)
        test_get_selected_menu_item(self, "c", menu.create_project)
        test_get_selected_menu_item(self, "v", menu.enter_votes)
        test_get_selected_menu_item(self, "s", menu.show_project)
        test_get_selected_menu_item(self, "q", menu.quit_program)
        test_get_selected_menu_item(self, "C", menu.create_project)
        test_get_selected_menu_item(self, "  C ", menu.create_project)
