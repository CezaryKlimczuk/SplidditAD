import csv

from project import Person, Project


class ProjectsImporter:

    def __init__(self, file_name, projects_repo) -> None:
        super().__init__()
        self.file_name = file_name
        self.projects_repo = projects_repo

    def import_projects(self):
        try:
            projects = self.__read_projects()
        except MalformedCsvError:
            projects = []

        self.projects_repo.put(projects)

    def __read_projects(self):
        projects = []
        with open(self.file_name, mode="r", newline="\n") as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                project_name = row[0]
                member_count = int(row[1])
                members = []
                for member_index in range(member_count):
                    member_name = row[2 + member_index]
                    member = Person(member_name)
                    members.append(member)

                for i in range(member_count):
                    from_index = 2 + member_count + i * (1 + (member_count - 1) * 2)
                    to_index = from_index + (1 + (member_count - 1) * 2)
                    vote_section = row[from_index:to_index]
                    voter_name = vote_section[0]

                    for member in members:
                        if member.name == voter_name:
                            for target_member_name_index in range(0, (member_count - 1) * 2, 2):
                                target_member_name = vote_section[1 + target_member_name_index]
                                target_member_vote = vote_section[1 + target_member_name_index + 1]

                                for target_member in members:
                                    if target_member.name == target_member_name:
                                        member.votes[member] = int(target_member_vote)

                project = Project(project_name, members)
                project.calculate_shares()

        return projects


class MalformedCsvError(IOError):

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
