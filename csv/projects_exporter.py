import _csv
import os


class ProjectsExporter:

    def __init__(self, file_name, projects_repo) -> None:
        super().__init__()
        self.file_name = file_name
        self.projects_repo = projects_repo

    def export_projects(self):
        lines = []
        for project in self.projects_repo.get_all():
            try:
                lines.append(self.__to_csv_line(project))
            except ValueError as error:
                print(error)

        with self.__get_file() as f:
            csv_writer = _csv.writer(f)
            csv_writer.writerows(lines)

    @staticmethod
    def __to_csv_line(project):
        for member in project.members:
            if member.get_remaining_votes() != 0:
                # Cannot export projects where the user hasn't filled the votes
                raise ValueError("Cannot export project \"%s\" because the votes haven't been entered" % project.name)

        elements = [project.name, project.get_member_count()]

        # Appending member names
        for member in project.members:
            elements.append(member.name)

        # Appending votes for each member
        for member in project.members:
            elements.append(member.name)
            for (target_member, votes) in member.votes.items():
                elements.append(target_member.name)
                elements.append(votes)

        return elements

    def __get_file(self):
        if not os.path.exists(self.file_name):
            # when calling open() the "+" mode will create the file if it does not exist
            print("File \"%s\" does not exist to export projects. Creating file." % self.file_name)

        return open(self.file_name, mode='w+')
