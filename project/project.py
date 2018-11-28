MAX_AVAILABLE_VOTES = 100


class Project:
    MIN_MEMBER_COUNT = 3

    def __init__(self, project_name, members):
        self.name = project_name
        self.__assert_member_names_are_unique(members)
        self.__assert_enough_members(members)
        self.members = list(members)
        for member in members:
            member._project = self

    def __eq__(self, o: object) -> bool:
        if id(self) == id(o):
            return True

        if not isinstance(o, Project):
            return False

        if self.name != o.name:
            return False

        # we don't care about the order of the members, but we do need them to be ordered when testing. This is because
        # when assigning votes we need to know the order in which the program will ask the user to assign votes to
        # members in
        if set(self.members) != set(o.members):
            return False

        return True

    def __hash__(self) -> int:
        return hash(self.name)

    @staticmethod
    def __assert_member_names_are_unique(members):
        unique_member_names = set(map(lambda member: member.name, members))
        if len(unique_member_names) != len(members):
            raise ValueError("Duplicate member names in %s" % members)

    @staticmethod
    def __assert_enough_members(members):
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

    def show_details(self):
        """
        Prints the number of team members and the scores of each team member
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

        print(details)

    def __str__(self) -> str:
        return "Project(name=%s, members=%s)" % (self.name, str(self.members))
