MAX_AVAILABLE_VOTES = 100


class Project:
    """
    The Project class stores all the necessary info about a Project. It holds the name and all the members.
    Attempting to create an invalid Project, such as one with a name that is too short throws an exception.
    """

    MIN_MEMBER_COUNT = 3
    MIN_NAME_LENGTH = 3
    VALID_NAME_SPECIAL_CHARS = ['-', '_']

    def __init__(self, project_name, members):
        self.__name = self.__assert_valid_project_name(project_name)
        self.__assert_member_names_are_unique(members)
        self.__assert_enough_members(members)
        self.members = list(members)
        for member in members:
            member._project = self

    @property
    def name(self):
        """
        A getter for the project name

        :return: The project name. Does not contain whitespace
        """
        return self.__name

    def __eq__(self, o: object) -> bool:
        if id(self) == id(o):
            return True

        if not isinstance(o, Project):
            return False

        if self.__name != o.__name:
            return False

        # we don't care about the order of the members, but we do need them to be ordered when testing. This is because
        # when assigning votes we need to know the order in which the program will ask the user to assign votes to
        # members in
        if set(self.members) != set(o.members):
            return False

        return True

    def __hash__(self) -> int:
        # name is always unique in the repo, hash that directly
        return hash(self.__name)

    @staticmethod
    def __assert_valid_project_name(project_name: str):
        """
        Throws an exception if the project name is invalid.
        Returns the name that should be used, as it is trimmed (stripped) of whitespace

        :param project_name: The name of the project
        :return: The name of the project. May be different than the argument
        :raises ValueError if the name isn't valid
        """
        result = project_name.strip()

        if len(result) < Project.MIN_NAME_LENGTH:
            raise ValueError(
                "Project name '%s' is too short. Must be at least '%s' characters in length"
                % (result, Project.MIN_NAME_LENGTH)
            )

        for char in result:
            if not Project.__is_valid_char_name(char):
                raise ValueError(
                    "Invalid character '%s' in name '%s'. All chars must be alphanumeric, or '-', or '_'"
                    % (char, result)
                )

        return result

    @staticmethod
    def __is_valid_char_name(char):
        """
        Checks if a char is valid. A valid char is alphanumeric (any case) or in Project.VALID_NAME_SPECIAL_CHARS

        :param char: The characters in a name that we're testing if it's allowed
        :return: True if the character is allowed in the name, False otherwise.
        """
        return char.isalpha() or char.isnumeric() or char in Project.VALID_NAME_SPECIAL_CHARS

    @staticmethod
    def __assert_member_names_are_unique(members):
        """
        Asserts that all members have unique names. If there are duplicate member names, it raises a ValueError

        :param members: The members that the Project should have
        """
        unique_member_names = set(map(lambda member: member.name, members))
        if len(unique_member_names) != len(members):
            raise ValueError("Duplicate member names in %s" % members)

    @staticmethod
    def __assert_enough_members(members):
        """
        Asserts that we have enough members. If we don't have enough, a ValueError is raised

        :param members: The members that the Project should have
        """
        if len(members) < Project.MIN_MEMBER_COUNT:
            raise ValueError("Not enough members %s. Require at least %s" % (members, Project.MIN_MEMBER_COUNT))

    def get_member_count(self):
        """
        Returns the number of members in the project

        :return: int the number of members in the project
        """
        return len(self.members)

    def get_longest_member(self):
        """

        :return: a person who has the longest name in the project. If multiple people have the longest name,
        then the result is undefined
        """
        return max(self.members, key=lambda x: len(x.name))

    def get_details(self):
        """
        :return (string) a user-presentable string with the number of team members and the scores of each team member
        """
        details = ""
        details += "\n"
        details += ("There are %s team members\n" % self.get_member_count())
        details += "\n"
        details += "The point allocation based on votes is:\n"
        details += "\n"

        indent_left = "\t"
        longest_member = self.get_longest_member()
        indent_right = "\t"
        for member in self.members:
            name_space_count = len(longest_member.name) - len(member.name)
            str_right = ":" + name_space_count * " "
            details += (indent_left + member.name + str_right + indent_right + str(member.get_total_score(self))) + "\n"

        details += "\n"
        return details

    def __str__(self) -> str:
        return "Project(name=%s, members=%s)" % (self.__name, str(self.members))
