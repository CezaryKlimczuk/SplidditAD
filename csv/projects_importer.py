import _csv

from project.project import Project
from person.person import Person

debug = False


class ProjectsImporter:

    def __init__(self, file_name, projects_repo) -> None:
        """

        :param file_name: The name of the file, relative to the root directory of the program, from which it will
        parse the projects and add them into the projects_repo

         :param projects_repo: The repository to which the projects will be added to
        """
        super().__init__()
        self.__file_name = file_name
        self.__projects_repo = projects_repo

    def import_projects(self):
        print("Importing projects from %s" % self.__file_name)
        try:
            projects = self.__read_projects()
            self.__projects_repo.put(projects)
            print("Imported %s projects" % len(projects))
        except FileNotFoundError:
            print("File %s does not exist to import projects from" % self.__file_name)

    def __read_projects(self):
        """
        Opens the file and parses it to return the stored projects. Any parsing errors are printed to the console.
        If the file does not exist, a FileNotFoundError is raised.

        :return: a list of valid projects imported from the file
        """
        projects = []
        with open(self.__file_name, mode="r", newline="\n") as f:
            csv_reader = _csv.reader(f)
            for row in csv_reader:
                try:
                    project = self.__from_csv_line(row)
                    projects.append(project)
                except Exception as error:
                    print("Problem parsing \"%s\": %s" % (row, error))

            return projects

    @staticmethod
    def __from_csv_line(row):
        """
        Parses a single row to a Project, or raises an error if there is a problem parsing the row or the project is
        invalid

        :param row: A list of elements from a CSV file, as defined in the project brief
        :return: a valid Project if successfully parsed
        :raises an Exception when there is a problem parsing the row or the project with is invalid
        """
        project_name = row[0]
        member_count = int(row[1])

        # name + member_count + member names + member votes
        expected_row_size = 1 + 1 + member_count + member_count + member_count * (member_count - 1) * 2
        if expected_row_size != len(row):
            raise ValueError("Incorrect size. Expected=%s, actual=%s" % (expected_row_size, len(row)))

        members = {}  # member name -> member
        for member_index in range(member_count):
            member_name = row[2 + member_index]
            member = Person(member_name)
            members[member_name] = member

        for member_index in range(member_count):
            from_index = 2 + member_count + member_index * (1 + (member_count - 1) * 2)
            to_index = from_index + (1 + (member_count - 1) * 2)
            vote_section = row[from_index:to_index]
            voter_name = vote_section[0]
            if voter_name not in members:
                raise ValueError("Voter %s not in the members list" % voter_name)

            for member in members.values():
                if member.name == voter_name:
                    for target_member_name_index in range(0, (member_count - 1) * 2, 2):
                        target_member_name = vote_section[1 + target_member_name_index]
                        if target_member_name not in members:
                            raise ValueError("Target member %s isn't in the members list" % target_member_name)

                        target_member_vote = vote_section[1 + target_member_name_index + 1]

                        for target_member in members.values():
                            if target_member.name == target_member_name:
                                previous_vote = member.assign_votes(target_member, int(target_member_vote))
                                if previous_vote is not None:
                                    raise ValueError("Duplicate votes for %s" % member, target_member)

                    if member.remaining_votes != 0:
                        raise ValueError("Did not assign all votes for %s" % member)

        project = Project(project_name, members.values())
        return project
