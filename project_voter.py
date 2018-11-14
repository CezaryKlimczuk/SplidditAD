from project import MAX_AVAILABLE_VOTES


class ProjectVoter():

    def __init__(self) -> None:
        super().__init__()

    def assign_points_from_user(self, project):
        """
        Queries the user to assign votes for each member of the supplied project

        :param project: The project that the user has to fill in the votes for each member
        """
        # The process of assigning votes starts here
        points = []  # A list of the sum of votes given by each member
        points_assigned_correctly = False  # All values need to be equal to project.MAX_AVAILABLE_VOTES, ergo False
        while not points_assigned_correctly:
            # Iterating through all members in a project
            for assignor in project.members:
                print("\nEnter %s's votes, points must add up to %s:\n" % (assignor.name, MAX_AVAILABLE_VOTES))
                remaining_points = MAX_AVAILABLE_VOTES  # The number of disposable votes for each member
                # Iterating through all partners of a member
                remaining_members_count = len(project.members) - 2
                # This will be used to ensure that no partner is left with zero points (check WHILE NOT below)
                for assignee in project.members:
                    if assignee != assignor:
                        points_input = self.__get_assigned_points(assignor, assignee, remaining_points,
                                                                  remaining_members_count)

                        assignor.votes[assignee] = points_input  # Adding votes to a member
                        remaining_points -= points_input  # Decreasing the number of disposable votes left
                        remaining_members_count -= 1

                points.append(
                    MAX_AVAILABLE_VOTES - remaining_points)  # Adding the number of points given by each member (should be MAX_AVAILABLE_VOTES)

            points_assigned_correctly = True  # Assuming that all values in points are MAX_AVAILABLE_VOTES
            # Checking if each member's votes add up to MAX_AVAILABLE_VOTES.
            # If they don't, any changes are cancelled. Iterate through members again (while loop)
            for x in points:
                if x != MAX_AVAILABLE_VOTES:
                    points_assigned_correctly = False
                    print('\nPoints from every member have to add up to %s. Please try again.\n' % MAX_AVAILABLE_VOTES)
                    for any_member in project.members:
                        any_member.votes.clear()
                    points = []
                    break

    @staticmethod
    def __get_assigned_points(assignor, assignee, points_left, remaining_members_count):
        """
        Queries the user for points to allocate from assignor to assignee

        :param assignor: (Person) The project member who is giving points to the assignee
        :param assignee: (Person) The project member who is being given points by the assignor
        :param points_left: (int) The number of points the assignor has remaining to assign
        :param remaining_members_count: The number of members the assignor still has to allocate points to afterwards
        :return: (int) The number of points the assignor allocated to the assignee. Between 0 (inclusive) and points_left (inclusive)
        """
        points = input("Enter %s's points for %s:" % (assignor.name, assignee.name))
        # Validate:
        # Must be integer
        # Last member has exactly points_left assigned to sum up to MAX_AVAILABLE_VOTES
        # If not last member, desired assigned point count is within range
        while (not points.isdigit()) \
                or remaining_members_count == 0 and int(points) != points_left \
                or not (0 <= int(points) <= points_left):
            points = input("Incorrect input. Enter %s's points for %s:" % (assignor.name, assignee.name))

        return int(points)
