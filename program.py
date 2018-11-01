import menu
from project_creator import ProjectCreator
from project_repository import ProjectRepository
from project_retriever import ProjectRetriever
from project_voter import ProjectVoter

project_repo = ProjectRepository()
project_creator = ProjectCreator(project_repo)
project_retriever = ProjectRetriever(project_repo)
project_voter = ProjectVoter()


def main():
    """
    Most important part of the program. Responsible for the main menu
    """
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
        elif selected_option == menu.quit_program:
            on_quit()

        if selected_option != menu.quit_program:
            menu.await_input_for_main_menu()


def on_print_about_requested():
    """
    Prints information about the program, and awaits user input to return to the menu
    """
    about = "This is a Fair Grade Allocator. The purpose of the application is to help teams allocate the credit for a " \
            "project so that all parties are satisfied with the outcome. The idea is inspired by the work of " \
            "Ariel Procaccia, a professor, and Jonathan Goldman, a student, who were both at Carnegie Mellon " \
            "University in the USA (Jonathan now works for Facebook). They went on to produce a web application " \
            "called Spliddit which offers provably fair solutions for a variety of division problems including " \
            "rent payments, restaurant bills and shared tasks. You can use the website to find out how the fair " \
            "grade allocator works."

    print(about)


def on_create_project_requested():
    project_creator.create_new_project()


def on_enter_votes_requested():
    """
    Queries the user for a project name, finds the project, queries user for votes, and calculates finally calculated
    the share of each member in a given project
    """
    project = project_retriever.get_project_from_user()
    print('There are %s team members.' % project.get_member_count())
    project_voter.assign_points_from_user(project)

    # Masz tutaj wyniki gdybyś chciał sprawdzić jak to wszystko działa. Enjoy ^^
    for member in project.members:
        print('%s - %s' % (member.name, member.share))


def on_show_project_requested():
    """
    The user has requested to show a project
    """
    project = project_retriever.get_project_from_user()
    project.show_details()


def on_quit():
    project_repo.on_close()
    pass


if __name__ == '__main__':
    """
    The main entry point to the program
    """
    main()
