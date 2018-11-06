import builtins
from contextlib import contextmanager
from unittest import TestCase

import menu
from tests.test_helper import mock_inputs


class TestGetSelectedMenuItem(TestCase):

    def test_valid_input(self):
        """
        Tests all possible valid shortcuts
        Tests case sensitivity
        Tests whitespace

        """
        self.assert_returns_menu_item_for_input("a", menu.about)
        self.assert_returns_menu_item_for_input("c", menu.create_project)
        self.assert_returns_menu_item_for_input("v", menu.enter_votes)
        self.assert_returns_menu_item_for_input("s", menu.show_project)
        self.assert_returns_menu_item_for_input("q", menu.quit_program)
        self.assert_returns_menu_item_for_input("C", menu.create_project)
        self.assert_returns_menu_item_for_input("  C ", menu.create_project)

    def assert_returns_menu_item_for_input(self, mock_input_val, expected):
        """

        :param mock_input_val: What should be returned on the next call to input()
        :param expected: What we expect menu.get_selected_menu_item() to return for the mock_input_val
        """
        with mock_inputs([mock_input_val]):
            item = menu.get_selected_menu_item()
            self.assertEqual(item, expected)

    def test_invalid_input(self):
        """
        Tests invalid inputs ("p", "") and completes with valid input "v" (enter votes)
        """
        with mock_inputs(["p", "", "v"]):
            selected = menu.get_selected_menu_item()
            self.assertEqual(menu.enter_votes, selected)
