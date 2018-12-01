import builtins
from unittest import TestCase
from unittest.mock import MagicMock

from menu import menu
from menu.menu import MenuItem
from tests.test_helper import mock_inputs


class TestMenu(TestCase):

    def test_print_main_menu_calls_print(self):
        original_print = builtins.print
        builtins.print = MagicMock()

        menu.print_main_menu()
        self.assertTrue(builtins.print.called)
        
        builtins.print = original_print

    def test_get_selected_menu_for_default_valid_input(self):
        self.assert_returns_menu_item_for_input("a", MenuItem.ABOUT)
        self.assert_returns_menu_item_for_input("c", MenuItem.CREATE_PROJECT)
        self.assert_returns_menu_item_for_input("v", MenuItem.ENTER_VOTES)
        self.assert_returns_menu_item_for_input("s", MenuItem.SHOW_PROJECT)
        self.assert_returns_menu_item_for_input("q", MenuItem.QUIT_PROGRAM)

    def test_get_selected_menu_for_uppercase(self):
        self.assert_returns_menu_item_for_input("C", MenuItem.CREATE_PROJECT)

    def test_get_selected_menu_for_whitespace(self):
        self.assert_returns_menu_item_for_input("  C ", MenuItem.CREATE_PROJECT)

    def test_invalid_input(self):
        """
        Tests invalid inputs ("p", "") and completes with valid input "v" (enter votes)
        """
        with mock_inputs(["p", "", "v"]):
            selected = menu.get_selected_menu_item()
            self.assertEqual(MenuItem.ENTER_VOTES, selected)

    def assert_returns_menu_item_for_input(self, mock_input_val, expected):
        """

        :param mock_input_val: What should be returned on the next call to input()
        :param expected: What we expect menu.get_selected_menu_item() to return for the mock_input_val
        """
        with mock_inputs([mock_input_val]):
            item = menu.get_selected_menu_item()
            self.assertEqual(item, expected)
