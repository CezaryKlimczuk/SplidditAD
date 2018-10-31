about = 'A'
create_project = 'C'
enter_votes = 'V'
show_project = 'S'
quit_program = 'Q'

all_options = [about, create_project, enter_votes, show_project, quit_program]


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
    option = str(input("  Please choose an option: ")).upper().strip()
    while option not in all_options:
        option = str(input("  Incorrect input. Please choose an option: ")).upper().strip()
    return option


def await_input_for_main_menu():
    """
    Requests the user to input anything to return to the main menu
    """
    input('Press any key to return to the main menu: ')
