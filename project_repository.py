class ProjectRepository:

    def __init__(self) -> None:
        super().__init__()
        self.projects = []

    def put(self, project):
        self.projects.append(project)

    def delete(self, project):
        self.projects.remove(project)
