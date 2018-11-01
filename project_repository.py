class ProjectRepository:

    def __init__(self) -> None:
        super().__init__()
        self.__projects = []

    def put(self, projects):
        if hasattr(projects, "__iter__"):
            self.__projects.extend(projects)
        else:
            self.__projects.append(projects)

    def delete(self, project):
        self.__projects.remove(project)

    def delete_all(self):
        self.__projects.clear()

    def get_all(self):
        # TODO return a new projects list instead of existing, maybe via copy.deep_copy_list()?
        return self.__projects

    def find_by_name(self, name):
        """
        Finds a project for a given name

        :param name: The name of the project
        :return: The first project to be found with the given name, or None if there are none that have such a name
        """
        projects_for_name = (project for project in self.__projects if project.name == name)
        return next(projects_for_name, None)
