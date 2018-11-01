import csv
from _csv import writer

projects_file_name = "projects.csv"


class ProjectRepository:

    def __init__(self) -> None:
        super().__init__()
        self.__projects = []

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
        self.__save_projects()

    def __save_projects(self):
        lines = []
        for project in self.__projects:
            lines.append(project.to_csv_line())

        print(lines)

        with open(projects_file_name, "w", newline="\n") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(lines)
