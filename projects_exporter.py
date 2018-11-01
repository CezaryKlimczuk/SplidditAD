import csv


class ProjectsExporter:

    def __init__(self, file_name, projects_repo) -> None:
        super().__init__()
        self.file_name = file_name
        self.projects_repo = projects_repo

    def export_projects(self):
        lines = []
        for project in self.projects_repo.get_all():
            lines.append(self.__to_csv_line(project))

        with self.__get_file() as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(lines)

    @staticmethod
    def __to_csv_line(project):
        elements = [project.name, project.get_member_count()]

        # Appending member count + member names
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
        return open(self.file_name, mode="w", newline="\n")
