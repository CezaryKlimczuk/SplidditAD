from enum import Enum


class MenuItem(Enum):
    """
    An enum for each menu item
    """
    ABOUT = 'A'
    CREATE_PROJECT = 'C'
    ENTER_VOTES = 'V'
    SHOW_PROJECT = 'S'
    QUIT_PROGRAM = 'Q'

    @staticmethod
    def has_value(value):
        """
        Checks if any of the defined MenuItem enums have the same value as the argument.

        :param value: The argument we are searching for to see if an enum has it
        :return: True if such a MenuItem exists, False otherwise
        """
        return any(value == item.value for item in MenuItem)


def print_main_menu():
    """
    Prints the main menu
    """
    print('Welcome to Split-it\n\n'
          '  About           (A)\n'
          '  Create Project  (C)\n'
          '  Enter Votes     (V)\n'
          '  Show Project    (S)\n'
          '  Quit            (Q)\n')


def get_selected_menu_item():
    """
    Queries the user to enter the shortcut for a menu item. users query is case insensitive and whitespace is stripped.

    :return: an element of all_options
    """
    option = input("  Please choose an option: ").upper().strip()
    while not MenuItem.has_value(option):
        option = input("  Incorrect input. Please choose an option: ").upper().strip()

    return MenuItem(option)


def await_input_for_main_menu():
    """
    Requests the user to input anything to return to the main menu
    """
    input('Press any key to return to the main menu: ')
