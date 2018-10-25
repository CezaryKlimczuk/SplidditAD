class Project:
    def __init__(self, project_name, members):
        self.name = project_name
        self.members = members


class Person:
    def __init__(self, name):
        self.name = name
        self.points = 0


create_project = 'C'


def main_menu():
    print('Welcome to Split-it\n\n'
          '  About           (A)\n'
          '  Create Project  (C)\n'
          '  Enter Votes     (V)\n'
          '  Show Project    (S)\n'
          '  Quit            (Q)\n')
    options = ['A', create_project, 'V', 'S', 'Q']
    option = str(input("  Please choose an option: ")).upper()
    while option not in options:
        option = str(input("  Incorrect input. Please choose an option: ")).upper()
    return option


def about():
    print('All of the information is here!!!')
    any_key = input('Press any key to return to the main menu: ')
    if type(any_key) == str:
        pass


def create_new_project():
    project_name = str(input("Enter the project name: "))
    num_of_members = input("Enter the number of team members: ")
    while not num_of_members.isdigit():
        num_of_members = input("Incorrect input. Please enter the number of team members: ")
    num_of_members = int(num_of_members)
    team_members = []
    print('\n')
    for i in range(num_of_members):
        member_name = str(input("     Enter the name of team member {}: ".format(i + 1)))
        team_members.append(Person(member_name))
    print('\n')
    any_key = input('Press any key to return to the main menu: ')
    if type(any_key) == str:
        return Project(project_name, team_members)


# programme goes here

option = ""
projects = []
while option != 'Q':
    option = main_menu()
    if option == 'A':
        about()
    elif option == create_project:
        projects.append(create_new_project())
    else:
        print("TODO")

print(projects[0].name)
print(projects[0].members[0].name)
