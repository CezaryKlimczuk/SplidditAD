class Project:
    def __init__(self, project_name, members):
        self.name = project_name
        self.members = members

    def get_member_count(self):
        return len(self.members)


class Person:
    def __init__(self, name):
        self.name = name
        self.votes = []
        self.share = 0


option_about = 'A'
option_create_project = 'C'
option_enter_votes = 'V'
option_show_project = 'S'
option_quit = 'Q'

all_options = [option_about, option_create_project, option_enter_votes, option_show_project, option_quit]

projects = []


def print_main_menu():
    print('Welcome to Split-it\n\n'
          '  About           (A)\n'
          '  Create Project  (C)\n'
          '  Enter Votes     (V)\n'
          '  Show Project    (S)\n'
          '  Quit            (Q)\n')


def get_selected_menu_item():
    option = str(input("  Please choose an option: ")).upper().strip()
    while option not in all_options:
        option = str(input("  Incorrect input. Please choose an option: ")).upper().strip()
    return option


def print_about():
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


def is_member_count_input_valid(member_count_input) -> bool:
    """
    Checks if the users input for the number of members is valid

    :param member_count_input: A (str) which represents the users input when queried for the number
    of members in the project
    :return: True if the input is an integer and is valid
    """
    return member_count_input.isdigit() and int(member_count_input) > 2


def create_new_project():
    """
    Queries the user to create a new project. The name might be the same as a previous project.
    It does not add the returned Project to a repository, this is left to the caller

    :return: a new Project
    """
    # TODO project name must be unique. Update documentation when fixed
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
    project_members = []
    for member_index in range(num_of_members):
        member = get_project_member(member_index, project_members)
        project_members.append(member)

    return project_members


def get_project_member(member_index, current_team_members):
    """
    Queries the user for a member name until it is unique and returns a new Person

    :param member_index: (int) a non-negative integer  indicating the position in current_team_members that the member represents
    :param current_team_members: a list of team members entered so far
    :return: a Person which has a unique name not currently present in current_team_members
    """
    member_name = str(input("     Enter the name of team member %s: " % (member_index + 1)))
    # Checking if the same member is not entered twice
    while member_name in [member.name for member in current_team_members]:
        member_name = str(
            input(
                "     %s already in the team. Enter the name of team member %s: " % (member_name, member_index + 1)))
    return Person(member_name)


def get_new_project_name():
    """
    Queries the user for a new project name.

    :return:
        (str) the project name. Can be empty or the same as a previous project name
    """
    return str(input("Enter the project name: "))


def get_new_project_member_count():
    """
    Queries the user for the number of members for a new project

    :return:
        (int) the number of members the new project should have. Will be at least 3
    """
    num_of_members = input("Enter the number of team members: ")
    while not is_member_count_input_valid(num_of_members):
        num_of_members = input("Incorrect input. Please enter the number of team members: ")
    num_of_members = int(num_of_members)
    return num_of_members


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


def enter_votes():
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
    # Checking if the name is in the list
    while name not in [x.name for x in projects]:
        name = input('Incorrect project name, please enter the project name:')
    # Finding a project in the list
    chosen_project = [x for x in projects if x.name == name][0]
    return chosen_project


def main():
    """
    Most important part of the program. Responsible for the main menu
    """
    selected_option = None
    while selected_option != option_quit:
        print_main_menu()
        selected_option = get_selected_menu_item()

        if selected_option == option_about:
            print_about()
        elif selected_option == option_create_project:
            projects.append(create_new_project())  # Adds a new project object to the list
        elif selected_option == option_enter_votes:
            enter_votes()


if __name__ == '__main__':
    """
    The main entry point to the program
    """
    main()
