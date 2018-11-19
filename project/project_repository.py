from project.project import Project


class ProjectRepository:

    def __init__(self) -> None:
        super().__init__()
        self.__projects = {}

    def put(self, what):
        if hasattr(what, "__iter__"):
            for project in what:
                self.put(project)
        elif type(what) is Project:
            self.__projects[what.name] = what
        else:
            raise ValueError("Incorrect type %s" % type(what))

    def delete(self, project):
        self.__projects.pop(project.name)

    def delete_all(self):
        self.__projects.clear()

    def get_all(self):
        return set(self.__projects.values())

    def find_by_name(self, name):
        """
        Finds a project for a given name

        :param name: The name of the project
        :return: The first project to be found with the given name, or None if there are none that have such a name
        """
        return self.__projects.get(name)
