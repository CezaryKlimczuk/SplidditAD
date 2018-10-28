from unittest import TestCase
from unittest.mock import patch

from UCL_project import *


class TestGetSelectedMenuItem(TestCase):

    @patch("UCL_project.get_input", return_value="a")
    def test_get_selected_menu_item_returns_about_for_a(self, input):
        item = get_selected_menu_item()
        self.assertEqual(item, option_about)

    @patch("UCL_project.get_input", return_value="c")
    def test_get_selected_menu_item_returns_create_for_c(self, input):
        item = get_selected_menu_item()
        self.assertEqual(item, option_create_project)

    @patch("UCL_project.get_input", return_value="v")
    def test_get_selected_menu_item_returns_enter_votes_for_v(self, input):
        item = get_selected_menu_item()
        self.assertEqual(item, option_enter_votes)

    @patch("UCL_project.get_input", return_value="s")
    def test_get_selected_menu_item_returns_show_project_for_s(self, input):
        item = get_selected_menu_item()
        self.assertEqual(item, option_show_project)

    @patch("UCL_project.get_input", return_value="q")
    def test_get_selected_menu_item_returns_quit_for_q(self, input):
        item = get_selected_menu_item()
        self.assertEqual(item, option_quit)

    @patch("UCL_project.get_input", return_value="C")
    def test_get_selected_menu_item_returns_create_for_capital(self, input):
        item = get_selected_menu_item()
        self.assertEqual(item, option_create_project)

    @patch("UCL_project.get_input", return_value="  C  ")
    def test_get_selected_menu_item_returns_create_for_white_space(self, input):
        item = get_selected_menu_item()
        self.assertEqual(item, option_create_project)
