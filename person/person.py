from project.project import MAX_AVAILABLE_VOTES


class Person:
    def __init__(self, name):
        self.name = name
        self.__votes = {}  # Person -> points (int)
        self.__remaining_votes = MAX_AVAILABLE_VOTES

    @property
    def votes(self):
        return self.__votes

    def get_remaining_votes(self):
        return self.__remaining_votes

    def __eq__(self, o: object) -> bool:
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
        if vote < 0:
            raise ValueError("Cannot assign negative votes")

        original_vote = self.__votes.get(person, None)
        if original_vote is not None:
            print("Updating score for %s" % person.name)
            if vote - original_vote > self.__remaining_votes:
                raise ValueError(
                    "%s: You've currently assigned %s votes for member %s and have %s points remaining to allocate, "
                    "but if you assign %s votes to them. you will not have enough points" % (
                        self.name, original_vote, person.name, self.__remaining_votes, vote))

            self.__remaining_votes += (original_vote - vote)
        else:
            # Check now whether we have enough votes
            if vote > self.__remaining_votes:
                raise ValueError("Cannot assign more votes than are available")
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
                vote = voter.__votes[self]
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