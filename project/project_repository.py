from project.project import Project


class ProjectRepository:
    """
    A ProjectRepository holds the Projects. It exposes all necessary CRUD operations for the Projects.
    Each Project in the repository has a unique name.

    Note that ideally it would be also responsible for importing/exporting the projects from a CSV file when needed,
    i.e. once at start up, and then each time a Project is touched. However, project requirements dictate that the
    Projects should be exported when quiting the Program, rather than  on the go (which would be better in case of a
    sudden termination)
    """

    def __init__(self) -> None:
        super().__init__()
        self.__projects = {}

    @property
    def projects(self):
        """

        :return: a copy of all Projects as a set. Modifying this set has no relation to the Projects stored in the
        repository.
        """
        return set(self.__projects.values())

    def put(self, what):
        """
        Puts a Project or Projects (via an iterable) into the repository. The project names must be unique.
        Otherwise, the most recent Project with the same name overrides the last project with the given name.

        :param what: a Project or (if needed infinitely nestable) iterable of Projects
        :raises ValueError when we attempt to put something that isn't an iterable and isn't a Project
        """
        if hasattr(what, "__iter__"):
            for project in what:
                self.put(project)
        elif type(what) is Project:
            self.__projects[what.name] = what
        else:
            raise ValueError("Incorrect type %s" % type(what))

    def delete(self, project):
        """
        Deletes the given project. If the project doesn't exist in the repository then nothing happens.

        :param project: The Project we wish to delete.
        """
        self.__projects.pop(project.name)

    def delete_all(self):
        """
        Deletes all projects from the repository.
        """
        self.__projects.clear()

    def find_by_name(self, name):
        """
        Finds a project for a given name

        :param name: The name of the project
        :return: The first project to be found with the given name, or None if there are none that have such a name
        """
        return self.__projects.get(name)
