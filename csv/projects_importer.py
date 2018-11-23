import _csv

from project.project import Project
from person.person import Person

debug = False


class ProjectsImporter:

    def __init__(self, file_name, projects_repo) -> None:
        super().__init__()
        self.__file_name = file_name
        self.__projects_repo = projects_repo

    def import_projects(self):
        try:
            projects = self.__read_projects()
        except FileNotFoundError:
            print("File %s does not exist to import projects from" % self.__file_name)
            projects = []

        self.__projects_repo.put(projects)

    def __read_projects(self):
        projects = []
        with open(self.__file_name, mode="r", newline="\n") as f:
            csv_reader = _csv.reader(f)
            for row in csv_reader:
                try:
                    project = self.__from_csv_line(row)
                    projects.append(project)
                except Exception:
                    pass

            return projects

    @staticmethod
    def __from_csv_line(row):
        project_name = row[0]
        member_count = int(row[1])

        # name + member_count + member names + member votes
        expected_row_size = 1 + 1 + member_count + member_count + member_count * (member_count - 1) * 2
        if expected_row_size != len(row):
            raise ValueError("Incorrect size. Expected=%s, actual=%s for \"%s\"" % (expected_row_size, len(row), row))

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

                    if member.get_remaining_votes() != 0:
                        raise ValueError("Did not assign all votes for %s" % member)

        project = Project(project_name, members.values())
        return project
