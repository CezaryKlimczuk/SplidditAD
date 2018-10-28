import builtins
from contextlib import contextmanager
from unittest import TestCase

from UCL_project import *


@contextmanager
def mock_input(mock):
    original_input = builtins.input
    builtins.input = lambda _: mock
    yield
    builtins.input = original_input


def test_get_selected_menu_item(test_case: TestCase, mock_input_val, expected):
    with mock_input(mock_input_val):
        item = get_selected_menu_item()
        test_case.assertEqual(item, expected)


class TestGetSelectedMenuItem(TestCase):

    def test_get_selected_menu_item_returns_about_for_a(self):
        test_get_selected_menu_item(self, "a", option_about)
        test_get_selected_menu_item(self, "c", option_create_project)
        test_get_selected_menu_item(self, "v", option_enter_votes)
        test_get_selected_menu_item(self, "s", option_show_project)
        test_get_selected_menu_item(self, "q", option_quit)
        test_get_selected_menu_item(self, "C", option_create_project)
        test_get_selected_menu_item(self, "  C ", option_create_project)
