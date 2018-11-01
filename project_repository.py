import csv
from _csv import writer

from project import Project, Person

projects_file_name = "projects.csv"


class ProjectRepository:

    def __init__(self) -> None:
        super().__init__()
        self.__projects = self.__read_projects()

    def put(self, project):
        self.__projects.append(project)

    def delete(self, project):
        self.__projects.remove(project)

    def find_by_name(self, name):
        """
        Finds a project for a given name

        :param name: The name of the project
        :return: The first project to be found with the given name, or None if there are none that have such a name
        """
        projects_for_name = (project for project in self.__projects if project.name == name)
        return next(projects_for_name, None)

    def on_close(self):
        self.__write_projects()

    def __write_projects(self):
        lines = []
        for project in self.__projects:
            lines.append(project.to_csv_line())

        print(lines)

        with open(projects_file_name, mode="w", newline="\n") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(lines)

    @staticmethod
    def __read_projects():
        projects = []
        with open(projects_file_name, mode="r", newline="\n") as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                print(row)
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
                                print(1 + target_member_name_index, vote_section)
                                target_member_name = vote_section[1 + target_member_name_index]
                                target_member_vote = vote_section[1 + target_member_name_index + 1]

                                for target_member in members:
                                    if target_member.name == target_member_name:
                                        member.votes[member] = int(target_member_vote)

                project = Project(project_name, members)
                project.calculate_shares()
                print(project)

        return projects


class MalformedCsvError(IOError):

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
