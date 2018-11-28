from project.project import Project
from person.person import Person


class ProjectCreator:

    def __init__(self, repo) -> None:
        """
        Create a new ProjectCreator, which is responsible for Querying the user to create a new, valid project.
        The project is added to  the repository by the ProjectCreator

        :param repo: The ProjectRepository that will be used to add the project to
        """
        super().__init__()
        self.__repo = repo

    def create_new_project(self):
        """
        Queries the user to create a new, valid project, and adds the project to the repository

        :return: a new Project
        """
        while True:
            project_name = self.__get_new_project_name()
            num_of_members = self.__get_new_project_member_count()
            print('\n')
            team_members = self.__get_new_project_member_names(num_of_members)
            print('\n')
            try:
                project = Project(project_name, team_members)
                self.__repo.put(project)
                return project
            except ValueError as error:
                print("Could not create project:")
                print(error)
                print("\n")

    def __get_new_project_name(self):
        """
        Queries the user for a new project name.

        :return: (str) the project name. Can be empty and will always have whitespace trimmed.
        """
        name = str(input("Enter the project name: ")).strip()

        # Make sure a project with such name doesn't exist
        while self.__repo.find_by_name(name) is not None:
            name = str(input("A project with this name already exists, try again."))

        # validation is performed when we try to create a Person with the name
        return name

    def __get_new_project_member_count(self):
        """
        Queries the user for the number of members for a new project

        :return:
            (int) the number of members the new project should have. Will be at least Project.MIN_MEMBER_COUNT
        """
        num_of_members = input("Enter the number of team members: ")
        while not self.__is_member_count_input_valid(num_of_members):
            num_of_members = input("Incorrect input. Please enter the number of team members: ")
        num_of_members = int(num_of_members)
        return num_of_members

    @staticmethod
    def __is_member_count_input_valid(member_count_input) -> bool:
        """
        Checks if the users input for the number of members is valid

        :param member_count_input: A (str) which represents the users input when queried for the number
        of members in the project
        :return: True if the input is an integer and is valid
        """
        return member_count_input.isdigit() and int(member_count_input) >= Project.MIN_MEMBER_COUNT

    def __get_new_project_member_names(self, num_of_members):
        """
        Gets the names of the project members from the user and validates the inputs

        :param num_of_members: (int) how many unique member names there will be in the project
        :return: a list of size num_of_members containing unique entries
        """
        project_members = []
        for member_index in range(num_of_members):
            member = self.__get_project_member(member_index, project_members)
            project_members.append(member)

        return project_members

    @staticmethod
    def __get_project_member(member_index, current_team_members):
        """
        Queries the user for a member name until it is unique and returns a new Person.
        Tha name is trimmed of whitespace.

        :param member_index: (int) a non-negative integer  indicating the position in current_team_members that
               the member represents
        :param current_team_members: a list of team members entered so far
        :return: a Person which has a unique name not currently present in current_team_members
        """
        while True:
            member_name = input("\tEnter the name of team member %s: " % (member_index + 1)).strip()

            # Checking if the same member is not entered twice
            if member_name in [member.name for member in current_team_members]:
                print("\t%s is already in the team." % member_name)
                continue

            try:
                person = Person(member_name)
                return person
            except ValueError as error:
                print(error)
