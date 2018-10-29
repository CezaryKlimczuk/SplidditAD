from project_creator import ProjectCreator
from project_repository import ProjectRepository

option_about = 'A'
option_create_project = 'C'
option_enter_votes = 'V'
option_show_project = 'S'
option_quit = 'Q'

all_options = [option_about, option_create_project, option_enter_votes, option_show_project, option_quit]

project_repo = ProjectRepository()
project_manager = ProjectCreator(project_repo)


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


def on_print_about_requested():
    """
    Prints information about the program, and awaits user input to return to the menu
    """
    about = "This is a Fair Grade Allocator. The purpose of the application is to help teams allocate the credit for a " \
            "project so that all parties are satisfied with the outcome. The idea is inspired by the work of " \
            "Ariel Procaccia, a professor, and Jonathan Goldman, a student, who were both at Carnegie Mellon " \
            "University in the USA (Jonathan now works for Facebook). They went on to produce a web application " \
            "called Spliddit which offers provably fair solutions for a variety of division problems including " \
            "rent payments, restaurant bills and shared tasks. You can use the website to find out how the fair " \
            "grade allocator works."

    print(about)
    await_input_for_main_menu()


def await_input_for_main_menu():
    """
    Requests the user to input anything to return to the main menu
    """
    input('Press any key to return to the main menu: ')


def assign_points_from_user(project):
    """
    Queries the user to assign votes for each member of the supplied project

    :param project: The project that the user has to fill in the votes for each member
    """
    # The process of assigning votes starts here
    points = []  # A list of the sum of votes given by each member
    points_assigned_correctly = False  # All values need to be equal to 100, ergo False
    while not points_assigned_correctly:
        # Iterating through all members in a project
        for assignor in project.members:
            print("\nEnter %s's votes, points must add up to 100:\n" % assignor.name)
            remaining_points = 100  # The number of disposable votes for each member
            # Iterating through all partners of a member
            remaining_members_count = len(project.members) - 2
            # This will be used to ensure that no partner is left with zero points (check WHILE NOT below)
            for assignee in project.members:
                if assignee != assignor:
                    points_input = get_assigned_points(assignor, assignee, remaining_points, remaining_members_count)

                    assignee.votes.append(points_input)  # Adding votes to a member
                    remaining_points -= points_input  # Decreasing the number of disposable votes left
                    remaining_members_count -= 1

            points.append(100 - remaining_points)  # Adding the number of points given by each member (should be 100)

        points_assigned_correctly = True  # Assuming that all values in points are 100
        # Checking if each member's votes add up to 100.
        # If they don't, any changes are cancelled. Iterate through members again (while loop)
        for x in points:
            if x != 100:
                points_assigned_correctly = False
                print('\nPoints from every member have to add up to 100. Please try again.\n')
                for any_member in project.members:
                    any_member.votes = []
                points = []
                break


def get_assigned_points(assignor, assignee, points_left, remaining_members_count):
    """
    Queries the user for points to allocate from assignor to assignee

    :param assignor: (Person) The project member who is giving points to the assignee
    :param assignee: (Person) The project member who is being given points by the assignor
    :param points_left: (int) The number of points the assignor has remaining to assign
    :param remaining_members_count: The number of members the assignor still has to allocate points to afterwards
    :return: (int) The number of points the assignor allocated to the assignee. Between 0 (inclusive) and points_left (inclusive)
    """
    points = input("Enter %s's points for %s:" % (assignor.name, assignee.name))
    # Validate:
    # Must be integer
    # Last member has exactly points_left assigned to sum up to 100
    # If not last member, desired assigned point count is within range
    while (not points.isdigit()) \
            or remaining_members_count == 0 and int(points) != points_left \
            or not (0 <= int(points) <= points_left):
        points = input("Incorrect input. Enter %s's points for %s:" % (assignor.name, assignee.name))

    return int(points)


def on_enter_votes_requested():
    """
    Queries the user for a project name, finds the project, queries user for votes, and calculates finally calculated
    the share of each member in a given project
    """
    project = get_project_from_user()
    print('There are %s team members.' % project.get_member_count())
    assign_points_from_user(project)

    # Calculate and store the share for each member
    for member in project.members:
        denominator = 1
        for vote in member.votes:
            denominator += (100 - vote) / vote
        member.share = round(1 / denominator, 2)  # Rounding member's share to 2 decimal places

    # Masz tutaj wyniki gdybyś chciał sprawdzić jak to wszystko działa. Enjoy ^^
    for member in project.members:
        print('%s - %s' % (member.name, member.share))


def get_project_from_user():
    """
    Queries the user for a project name and returns the first project that has that name.

    :return: a Project
    """
    name = input('Enter the project name: ')
    project = project_repo.find_by_name(name)

    while project is None:
        name = input('Incorrect project name, please enter the project name:')
        project = project_repo.find_by_name(name)

    return project


def on_show_project_requested():
    """
    The user has requested to show a project
    """
    project = get_project_from_user()
    show_project_details(project)


def show_project_details(project):
    """
    Prints the number of team members and the scores of each team member

    :param project: The project which should be displayed in the console
    """
    print("\n")
    print("There are %s team members" % project.get_member_count())  # At least 3 team members so always plural
    print("\n")
    print("The point allocation based on votes is:")
    print("\n")

    indent_left = "\t"
    longest_member = project.get_longest_member()
    indent_right = "\t"
    for member in project.members:
        name_space_count = len(longest_member.name) - len(member.name)
        str_right = ":" + name_space_count * " "
        print(indent_left + member.name + str_right + indent_right + str(member.get_total_score()))

    print("\n")
    await_input_for_main_menu()


def main():
    """
    Most important part of the program. Responsible for the main menu
    """
    selected_option = None
    while selected_option != option_quit:
        print_main_menu()
        selected_option = get_selected_menu_item()

        if selected_option == option_about:
            on_print_about_requested()
        elif selected_option == option_create_project:
            on_create_project_requested()
        elif selected_option == option_enter_votes:
            on_enter_votes_requested()
        elif selected_option == option_show_project:
            on_show_project_requested()


def on_create_project_requested():
    project_manager.create_new_project()
    await_input_for_main_menu()


if __name__ == '__main__':
    """
    The main entry point to the program
    """
    main()
