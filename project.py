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
