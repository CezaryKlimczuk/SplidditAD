MAX_AVAILABLE_VOTES = 100


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
        self.__votes = {}  # Person -> points (int)
        self.__remaining_votes = MAX_AVAILABLE_VOTES

    def get_remaining_votes(self):
        return self.__remaining_votes

    def __eq__(self, o: object) -> bool:
        # TODO test
        if id(self) == id(o):
            return True

        if not isinstance(o, Person):
            return False

        if self.name != o.name:
            return False

        if len(self.__votes) != len(o.__votes):
            return False

        for (self_person, self_vote) in self.__votes.items():
            found = False
            for (person, vote) in o.__votes.items():
                if self_person.name == person.name:
                    found = True
                    if self_vote != vote:
                        return False
            if not found:
                return False

        return True

    def __hash__(self) -> int:
        return hash(self.name)

    def assign_votes(self, person, vote):
        """
        Assigns votes from this instance to the argument person instance

        :param vote: The number of votes we want to assign to the other person
        :param person:  The person who we are assigning the votes to :param vote: The votes. Int between 0 (
        inclusive) and MAX_AVAILABLE_VOTES (inclusive)

        :return int: The previous vote that had been assigned to the above user.
                     If there was no previous result, None is returned
        """
        if vote > self.__remaining_votes:
            raise ValueError("Cannot assign more votes than are available")

        if vote < 0:
            raise ValueError("Cannot assign negative votes")

        original_vote = self.__votes.get(person, None)
        if original_vote is not None:
            print("Updating score for %s" % person.name)
            self.__remaining_votes += (original_vote - vote)
        else:
            self.__remaining_votes -= vote

        self.__votes[person] = vote
        return original_vote

    def get_total_score(self, project):
        """
        Calculates and returns the score using the share

        :exception Raises a ValueError if the member hasn't finished voting
        :return: (int) The score of the member. Is between 0 (inclusive) and MAX_AVAILABLE_VOTES (inclusive)
        """
        if self.__remaining_votes != 0:
            msg = "Member \"%s\" has't entered all their votes. They have %s points left to assign" % (
                self.name,
                self.__remaining_votes
            )
            raise ValueError(msg)

        denominator = 1
        for voter in project.members:
            if voter != self:
                vote = voter.votes[self]
                denominator += (MAX_AVAILABLE_VOTES - vote) / vote

        share = round(1 / denominator, 2)  # Rounding member's share to 2 decimal places

        return round(share * MAX_AVAILABLE_VOTES)

    def __str__(self) -> str:
        votes = ""
        for (index, (member, vote)) in enumerate(self.__votes.items()):
            votes += member.name + ": " + str(vote)
            if index != len(self.__votes) - 1:
                votes += ", "

        return "Person(name=%s, votes={%s})" % (self.name, votes)

    def __repr__(self) -> str:
        # TODO
        votes = ""
        for (member, vote) in self.__votes.items():
            votes += member.name + ": " + str(vote)

        return "Person(name=%s, votes={%s})" % (self.name, votes)
