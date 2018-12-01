from project.project import MAX_AVAILABLE_VOTES


class Person:
    MIN_NAME_LENGTH = 2
    VALID_SPECIAL_NAME_CHARS = ['-', '_']

    def __init__(self, name):
        """

        :param name: The name of the Person. Must be unique in a single project, but doesn't have to be unique across
        projects. The name must also be at least a certain number of characters in length, as defined in MIN_NAME_LENGTH
        """
        self.__name = Person.__assert_valid_name(name)
        self.__votes = {}  # Person -> points (int)
        self.__remaining_votes = MAX_AVAILABLE_VOTES

    @staticmethod
    def __assert_valid_name(name: str):
        """
        Asserts that the name is valid for a new Person.

        :param name: The name of the Person we wish to create.
        :return a name without whitespace
        :raises ValueError if the name is too short
        """
        if len(name.strip()) < Person.MIN_NAME_LENGTH:
            raise ValueError(
                "Name \"%s\" is too short. Must be at least %s characters in length (without whitespace)" %
                (name.strip(), Person.MIN_NAME_LENGTH)
            )

        for char in name.strip():
            if not Person.__is_valid_char_in_name(char):
                raise ValueError(
                    "Name '%s' contains invalid character '%s'. Only lowercase and uppercase names are allowed, as well as '-' and '_'" % (
                        name.strip(), char)
                )

        return name.strip()

    @staticmethod
    def __is_valid_char_in_name(char):
        """
        Check if a character in the Project name is valid.
        Valid characters are alphanumeric (any case) or '-', or '_'

        :param char: The character that we are checking if the name can contain
        :return: True if the given character can be in the project name, False otherwise
        """
        return char.isalpha() or char.isnumeric() or char in Person.VALID_SPECIAL_NAME_CHARS

    @property
    def votes(self):
        """
        A getter for self.__votes. This is a dictionary mapping a Person to an Integer. The key (Person) is who the
        current Person instance has voted on, and the value is how many points they have assigned

        :return: A dictionary mapping a Person (vote target) to an Integer (assigned points)
        """
        return self.__votes

    @property
    def name(self):
        """
        A getter for self.__name

        :return: (String) The persons name
        """
        return self.__name

    @property
    def remaining_votes(self):
        """
        A getter for self.__remaining_votes.

        :return: How many votes the person still has left to assign
        """
        return self.__remaining_votes

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
            if vote - original_vote > self.__remaining_votes:
                raise ValueError(
                    "%s: You've currently assigned %s votes for member %s and have %s points remaining to allocate, "
                    "but if you assign %s votes to them. you will not have enough points" % (
                        self.__name, original_vote, person.name, self.__remaining_votes, vote))

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
                self.__name,
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

        return "Person(name=%s, votes={%s})" % (self.__name, votes)

    def __repr__(self) -> str:
        votes = ""
        for (member, vote) in self.__votes.items():
            votes += member.name + ": " + str(vote)

        return "Person(name=%s, votes={%s})" % (self.__name, votes)

    def __eq__(self, o: object) -> bool:
        if id(self) == id(o):
            return True

        if not isinstance(o, Person):
            return False

        if self.__name != o.__name:
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
        # Names are unique, therefore just hash the name
        return hash(self.__name)
