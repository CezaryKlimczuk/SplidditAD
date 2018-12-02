class ProjectRetriever:
    """
    This class is responsible for querying the user for a project name and finding that project in the repository.
    Keeps querying the user for a valid input in case they give an incorrect response.
    """

    def __init__(self, repo) -> None:
        super().__init__()
        self.__repo = repo

    def get_project_from_user(self):
        """
        Queries the user for a project name and returns the first project that has that name. If there are no projects
        in the repository for the user to find, None is immediately returned.

        :return: a Project or None if there are no Projects in the repository
        """
        if len(self.__repo.projects) == 0:
            return None

        name = input('Enter the project name: ')
        project = self.__repo.find_by_name(name)

        while project is None:
            name = input('Incorrect project name, please enter the project name:')
            project = self.__repo.find_by_name(name)

        return project
