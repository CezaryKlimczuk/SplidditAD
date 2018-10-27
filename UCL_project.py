class Project:
    def __init__(self, project_name, members):
        self.name = project_name
        self.members = members


class Person:
    def __init__(self, name):
        self.name = name
        self.votes = []
        self.share = 0


option_create_project = 'C'
option_about = 'A'
option_enter_votes = 'V'
option_show_project = 'S'
option_quit = 'Q'

all_options = [option_about, option_create_project, option_enter_votes, option_show_project, option_quit]

selected_option = None
projects = []


def print_main_menu():
    print('Welcome to Split-it\n\n'
          '  About           (A)\n'
          '  Create Project  (C)\n'
          '  Enter Votes     (V)\n'
          '  Show Project    (S)\n'
          '  Quit            (Q)\n')


def get_selected_menu_item():
    option = str(input("  Please choose an option: ")).upper()
    while option not in all_options:
        option = str(input("  Incorrect input. Please choose an option: ")).upper()
    return option


def print_about():
    """
    Prints information about the program, and awaits user input to return to the menu
    """
    # TODO update program about
    print('All of the information is here!!!')
    await_input_for_main_menu()


def valid_member_count_input(member_count_input) -> bool:
    return member_count_input.isdigit() and int(member_count_input) > 2


def create_new_project():  # This function will return a project object, which will be added to projects list.
    project_name = get_new_project_name()
    num_of_members = get_new_project_member_count()
    print('\n')
    team_members = get_new_project_member_names(num_of_members)
    print('\n')
    await_input_for_main_menu()
    return Project(project_name, team_members)


def await_input_for_main_menu():
    """
    Requests the user to input anything to return to the main menu
    """
    input('Press any key to return to the main menu: ')


def get_new_project_member_names(num_of_members):
    """

    Gets the names of the project members from the user and validates the inputs

    :param num_of_members: (int) how many unique member names there will be in the project
    :return: a list of size num_of_members containing unique entries
    """
    team_members = []
    for i in range(num_of_members):
        member_name = str(input("     Enter the name of team member {}: ".format(i + 1)))
        # Checking if the same member is not entered twice
        while member_name in [member.name for member in team_members]:
            member_name = str(
                input("     {} already in the team. Enter the name of team member {}: ".format(member_name, i + 1)))
        team_members.append(Person(member_name))  # Adding Person object to the list of members
    return team_members


def get_new_project_name():
    """

    :return:
        (str) the project name. Can be empty or the same as a previous project name
    """
    return str(input("Enter the project name: "))


def get_new_project_member_count():
    """

    :return:
        (int) the number of members the new project should have. Will be at least 3
    """
    num_of_members = input("Enter the number of team members: ")
    while not valid_member_count_input(num_of_members):
        num_of_members = input("Incorrect input. Please enter the number of team members: ")
    num_of_members = int(num_of_members)
    return num_of_members


def enter_votes():  # This function calculates the share of each member in a given project
    name = input('Enter the project name: ')
    # Checking if the name is in the list
    while name not in [x.name for x in projects]:
        name = input('Incorrect project name, please enter the project name:')
    # Finding a project in the list
    chosen_project = [x for x in projects if x.name == name][0]
    num_of_members = len(chosen_project.members)
    print('There are {} team members.'.format(num_of_members))
    # The process of assigning votes starts here
    points_given = []  # A list of the sum of votes given by each member
    points_assigned_correctly = False  # All values need to be equal to 100, ergo False
    while not points_assigned_correctly:
        # Iterating through all members in a project
        for member in chosen_project.members:
            print("\nEnter {}'s votes, points must add up to 100:\n".format(member.name))
            points_left = 100  # The number of disposable votes for each member
            # Iterating through all partners of a member
            how_many_partners_left = len(chosen_project.members) - 2
            # This will be used to ensure that no partner is left with zero points (check WHILE NOT below)
            HMPL = how_many_partners_left
            for other_member in chosen_project.members:
                if other_member != member:
                    points = input("Enter {}'s points for {}:".format(member.name, other_member.name))
                    # Checking if the votes are non-negative
                    # And their sum is not greater than disposable votes
                    while not (points.isdigit() and 0 < int(points) <= points_left - HMPL):
                        points = input(
                            "Incorrect input. Enter {}'s points for {}:".format(member.name, other_member.name))
                    other_member.votes.append(int(points))  # Adding votes to a member
                    points_left -= int(points)  # Decreasing the number of disposable votes left
                    HMPL -= 1
            points_given.append(100 - points_left)  # Adding the number of points given by each member (should be 100)
        points_assigned_correctly = True  # Assuming that all values in points_given are 100
        # Checking if each member's votes add up to 100.
        # If they don't, any changes are cancelled. Iterate through members again (while loop)
        for x in points_given:
            if x != 100:
                points_assigned_correctly = False
                print('\nPoints from every member have to add up to 100. Please try again.\n')
                for any_member in chosen_project.members:
                    any_member.votes = []
                points_given = []
                break
    # If all votes have been assigned correctly, calculate the share of each member.
    # Store the share in Person object
    for member in chosen_project.members:
        denominator = 1
        for vote in member.votes:
            denominator += (100 - vote) / vote
        member.share = round(1 / denominator, 2)  # Rounding member's share to 2 decimal places
    # Masz tutaj wyniki gdybyś chciał sprawdzić jak to wszystko działa. Enjoy ^^
    for member in chosen_project.members:
        print('{} - {}'.format(member.name, member.share))
    return True


# programme goes here
while selected_option != option_quit:
    print_main_menu()
    selected_option = get_selected_menu_item()

    if selected_option == option_about:
        print_about()
    elif selected_option == option_create_project:
        projects.append(create_new_project())  # Adds a new project object to the list
    elif selected_option == option_enter_votes:
        enter_votes()
