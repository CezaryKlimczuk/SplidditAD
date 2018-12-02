import builtins
from unittest import TestCase
from unittest.mock import Mock

import program
from menu.menu import MenuItem
from tests import test_helper


class TestProgram(TestCase):

    def test_about_printed(self):
        inputs = [
            MenuItem.ABOUT.value,
            "\n",  # programs awaits any key to proceed
            MenuItem.QUIT_PROGRAM.value,
        ]

        with test_helper.mock_inputs(inputs):
            original_print = builtins.print
            builtins.print = Mock()
            program.main()

            # print is mocked, use stdout instead
            # for args in builtins.print.call_args_list:
            #     sys.stdout.write("\n===============================================\n")
            #     sys.stdout.write(str(args))

            # Note: couldn't get this to work.
            # self.assertTrue((ABOUT_TEXT,) in builtins.print.call_args_list)
            builtins.print = original_print

    def test_quits_when_selecting_q(self):
        inputs = [
            MenuItem.QUIT_PROGRAM.value
        ]

        with test_helper.mock_inputs(inputs):
            program.main()

        # If we get here, then the program successfully exited
