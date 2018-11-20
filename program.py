from menu import menu
from project.project_creator import ProjectCreator
from project.project_repository import ProjectRepository
from project.project_retriever import ProjectRetriever
from project.project_voter import ProjectVoter
from csv.projects_exporter import ProjectsExporter
from csv.projects_importer import ProjectsImporter

repo = ProjectRepository()
creator = ProjectCreator(repo)
retriever = ProjectRetriever(repo)
voter = ProjectVoter()
projects_file = "csv/projects.csv"
exporter = ProjectsExporter(projects_file, repo)
importer = ProjectsImporter(projects_file, repo)


def main():
    """
    Most important part of the program. Responsible for handling menu items.
    Once this method exits, the program is no longer running.

    on_start() is always called first

    on_print_about_requested()
    on_create_project_requested()
    on_enter_votes_requested()
    on_show_project_requested()
    are called for the corresponding menu items

    on_quit() is always called just before the program terminates from user selecting quit menu item
    """
    on_start()
    selected_option = None
    while selected_option != menu.quit_program:
        menu.print_main_menu()
        selected_option = menu.get_selected_menu_item()

        if selected_option == menu.about:
            on_print_about_requested()
        elif selected_option == menu.create_project:
            on_create_project_requested()
        elif selected_option == menu.enter_votes:
            on_enter_votes_requested()
        elif selected_option == menu.show_project:
            on_show_project_requested()

        if selected_option != menu.quit_program:
            menu.await_input_for_main_menu()

    on_quit()


def on_start():
    """
    Called whenever the program is started

    Project requirements state that the projects should be loaded from disk at this point
    """
    importer.import_projects()


def on_print_about_requested():
    """
    Prints information about the program
    """
    about = "This is a Fair Grade Allocator. The purpose of the application is to help teams allocate the credit for " \
            "a project so that all parties are satisfied with the outcome. The idea is inspired by the work of " \
            "Ariel Procaccia, a professor, and Jonathan Goldman, a student, who were both at Carnegie Mellon " \
            "University in the USA (Jonathan now works for Facebook). They went on to produce a web application " \
            "called Spliddit which offers provably fair solutions for a variety of division problems including " \
            "rent payments, restaurant bills and shared tasks. You can use the website to find out how the fair " \
            "grade allocator works."

    print(about)


def on_create_project_requested():
    """
    Queries the user to create a new project
    """
    creator.create_new_project()


def on_enter_votes_requested():
    """
    Queries the user for a project name, finds the project, queries user for votes, and updates the project.
    """
    project = retriever.get_project_from_user()
    print('There are %s team members.' % project.get_member_count())
    voter.assign_points_from_user(project)


def on_show_project_requested():
    """
    The user has requested to show a project
    """
    project = retriever.get_project_from_user()
    project.show_details()


def on_quit():
    """
    Called just before program terminates

    Program requirements dictate that projects should be exported to disk at this point
    """
    exporter.export_projects()


if __name__ == '__main__':
    """
    The main entry point to the program
    """
    main()
