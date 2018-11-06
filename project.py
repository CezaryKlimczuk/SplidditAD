class Project:
    def __init__(self, project_name, members):
        self.name = project_name

        self.__assert_member_names_are_unique(members)
        self.__assert_enough_members(members)
        self.members = members
        for member in members:
            member._project = self

    def __eq__(self, o: object) -> bool:
        # TODO test
        if id(self) == id(o):
            return True

        if not isinstance(o, Project):
            return False

        if self.name != o.name:
            return False

        if self.members != o.members:
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
        if len(members) < 3:
            raise ValueError("Not enough members %s. Require at least 3" % members)

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
            details += (indent_left + member.name + str_right + indent_right + str(member.get_total_score(self))) + "\n"

        details += "\n"

        print(details)

    def __str__(self) -> str:
        return "Project(name=%s, members=%s)" % (self.name, str(self.members))


class Person:
    def __init__(self, name):
        self.name = name
        self.votes = {}  # Person -> points (int)

    def __eq__(self, o: object) -> bool:
        # TODO test
        if id(self) == id(o):
            return True

        if not isinstance(o, Person):
            return False

        if self.name != o.name:
            return False

        if len(self.votes) != len(o.votes):
            return False

        for (self_person, self_vote) in self.votes.items():
            found = False
            for (person, vote) in o.votes.items():
                if self_person.name == person.name:
                    found = True
                    if self_vote != vote:
                        return False
            if not found:
                return False

        return True

    def __hash__(self) -> int:
        return hash(self.name)

    def get_total_score(self, project):
        """
        Calculates and returns the score using the share

        :return: (int) The score of the member. Is between 0 (inclusive) and 100 (inclusive)
        """
        denominator = 1
        for voter in project.members:
            if voter != self:
                vote = voter.votes[self]
                denominator += (100 - vote) / vote

        share = round(1 / denominator, 2)  # Rounding member's share to 2 decimal places

        return round(share * 100)

    def __str__(self) -> str:
        votes = ""
        for (index, (member, vote)) in enumerate(self.votes.items()):
            votes += member.name + ": " + str(vote)
            if index != len(self.votes) - 1:
                votes += ", "

        return "Person(name=%s, votes={%s})" % (self.name, votes)

    def __repr__(self) -> str:
        # TODO
        votes = ""
        for (member, vote) in self.votes.items():
            votes += member.name + ": " + str(vote)

        return "Person(name=%s, votes={%s})" % (self.name, votes)
