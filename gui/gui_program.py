import tkinter as tk


class SpliddItApp(tk.Frame):

    def __init__(self, master=tk.Tk()):
        super().__init__(master)
        self.pack()

        self.about = tk.Button(self)
        self.init_about()

        self.create_project = tk.Button(self)
        self.init_create_project()

        self.enter_votes = tk.Button(self)
        self.init_enter_votes()

        self.show_project = tk.Button(self)
        self.init_show_project()

        self.quit = tk.Button(self)
        self.init_quit()

    def init_about(self):
        self.about["text"] = "About"
        self.about["command"] = self.on_about_clicked
        self.about.pack(side="top")

    def init_create_project(self):
        self.create_project["text"] = "Create Project"
        self.create_project["command"] = self.on_create_project_clicked
        self.create_project.pack(after=self.about)

    def init_enter_votes(self):
        self.enter_votes["text"] = "Enter Votes"
        self.enter_votes["command"] = self.on_enter_votes_clicked
        self.enter_votes.pack(after=self.create_project)

    def init_show_project(self):
        self.show_project["text"] = "Show Project"
        self.show_project["command"] = self.on_show_project_clicked
        self.show_project.pack(after=self.enter_votes)

    def init_quit(self):
        self.quit["text"] = "Quit"
        self.quit["command"] = self.on_quit_clicked
        self.quit["fg"] = "#F00"
        self.quit.pack(after=self.show_project)

    def on_about_clicked(self):
        pass

    def on_create_project_clicked(self):
        pass

    def on_enter_votes_clicked(self):
        pass

    def on_show_project_clicked(self):
        pass

    def on_quit_clicked(self):
        self.master.destroy()
