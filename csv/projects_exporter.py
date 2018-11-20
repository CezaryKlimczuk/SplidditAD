import _csv
import os


class ProjectsExporter:
    """
    This class is responsible for exporting all the projects which are in the ProjectsRepo to the provided file.
    Ideally, the ProjectsRepo would be in control of persisting its state to io, however project requirements dictate
    that projects should be exported/imported at the start/exit of the program, rather than upon creating a new Project
    If the provided file does not exist, it creates it. If the files does exist, it is overwritten.

    The CSV file does not have a header line.
    The exact format is specified in Appendix 1 of the brief
    """

    def __init__(self, file_name, projects_repo) -> None:
        """
        Create a new ProjectsExporter to export projects to a CSV file

        :param file_name:
        :param projects_repo:
        """
        super().__init__()
        self.file_name = file_name
        self.projects_repo = projects_repo

    def export_projects(self):
        """
        Exports all the projects in the repo to the provided csv file. Overwrites any current such file.
        """
        print("Exporting %s projects to %s" % (len(self.projects_repo.get_all()), self.file_name))
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
        """
        Create a list of elements to export the given project to csv

        :param project: The project which we want to create a csv line from.
        :return: a list of strings which can be exported as csv by separating each element with a delimiter.
        :raises ValueError when the give project cannot be exported because the user hasn't entered all the votes.
        """
        for member in project.members:
            if member.get_remaining_votes() != 0:
                # Cannot export projects where the user hasn't filled the votes
                raise ValueError("Cannot export project \"%s\" because the votes haven't been entered" % project.name)

        # a list of values which will be stored in each line of the csv
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
        """
        Returns the file to write export the projects to.
        If the file exists, it will be overwritten.
        If it doesn't exist, it will be created

        :return: The file to be used to export the projects
        """
        if not os.path.exists(self.file_name):
            # when calling open() the "+" mode will create the file if it does not exist
            print("File \"%s\" does not exist to export projects. Creating file." % self.file_name)

        return open(self.file_name, mode='w+')
