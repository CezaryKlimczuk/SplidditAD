from project import Person, Project


def create_project(project_name, member_names):
    project_members = []
    for name in member_names:
        project_members.append(Person(name))

    return Project(project_name, project_members)
