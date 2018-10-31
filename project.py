class Project:
    def __init__(self, project_name, members):
        self.name = project_name
        self.members = members

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
        print(self)

    def __str__(self) -> str:
        details = ""
        details += "\n"
        details += ("There are %s team members\n" % self.get_member_count())  # At least 3 team members so always plural
        details += "\n"
        details += "The point allocation based on votes is:\n"
        details += "\n"

        indent_left = "\t"
        longest_member = self.get_longest_member()
        indent_right = "\t"
        for member in self.members:
            name_space_count = len(longest_member.name) - len(member.name)
            str_right = ":" + name_space_count * " "
            details += (indent_left + member.name + str_right + indent_right + str(member.get_total_score())) + "\n"

        details += "\n"
        return details


class Person:
    def __init__(self, name):
        self.name = name
        self.votes = []
        self.share = 0

    def get_total_score(self):
        """
        Calculates and returns the score using the share

        :return: (int) The score of the member. Is between 0 (inclusive) and 100 (inclusive)
        """
        return round(self.share * 100)
