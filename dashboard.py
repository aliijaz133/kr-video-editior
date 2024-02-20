import tkinter as tk
from tkinter import filedialog
import subprocess

class Dashboard:
    def __init__(self, master):
        self.master = master
        self.master.title("KR-Studio")

        self.project_name_label = tk.Label(self.master, text="Project Name:")
        self.project_name_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.project_name_entry = tk.Entry(self.master)
        self.project_name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.video_format_label = tk.Label(self.master, text="Video Format:")
        self.video_format_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.video_format_options = ["mp4", "mpg", "mpeg", "avi"]
        self.video_format_var = tk.StringVar(self.master)
        self.video_format_var.set(self.video_format_options[0])
        self.video_format_dropdown = tk.OptionMenu(self.master, self.video_format_var, *self.video_format_options)
        self.video_format_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        self.create_project_button = tk.Button(self.master, text="Create Project", command=self.create_project)
        self.create_project_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def create_project(self):
        project_name = self.project_name_entry.get()
        video_format = self.video_format_var.get()
        if project_name:
            # Create project and open it
            subprocess.run(["python", "video-editor.py", project_name, video_format])  # Pass project name as command-line argument
            self.master.destroy()
        else:
            tk.messagebox.showerror("Error", "Please enter a project name.")

def main():
    root = tk.Tk()
    root.geometry("720x720")
    app = Dashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
