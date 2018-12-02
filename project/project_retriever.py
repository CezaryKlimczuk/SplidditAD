class ProjectRetriever:
    """
    This class is responsible for querying the user for a project name and finding that project in the repository.
    Keeps querying the user for a valid input in case they give an incorrect response.
    """

    def __init__(self, repo) -> None:
        super().__init__()
        self.__repo = repo

    def get_project_from_user(self):
        # TODO what if there are no projects?
        """
        Queries the user for a project name and returns the first project that has that name.

        :return: a Project
        """
        name = input('Enter the project name: ')
        project = self.__repo.find_by_name(name)

        while project is None:
            name = input('Incorrect project name, please enter the project name:')
            project = self.__repo.find_by_name(name)

        return project
