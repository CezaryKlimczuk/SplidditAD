projects = []


class ProjectRepository:

    def put(self, project):
        projects.append(project)

    def delete(self, project):
        projects.remove(project)
