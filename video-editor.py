from tkinter import *
from tkinter import filedialog, messagebox
import sys
import pickle
import cv2
from PIL import Image, ImageTk
import os
import tkinter as tk
import webbrowser

class ExportDialog:
    def __init__(self, parent):
        self.parent = parent
        self.dialog = Toplevel(parent)
        self.dialog.title("Export Settings")

        self.width_label = Label(self.dialog, text="Width:")
        self.width_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)
        self.width_entry = Entry(self.dialog)
        self.width_entry.grid(row=0, column=1, padx=10, pady=5)

        self.height_label = Label(self.dialog, text="Height:")
        self.height_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)
        self.height_entry = Entry(self.dialog)
        self.height_entry.grid(row=1, column=1, padx=10, pady=5)

        self.frame_label = Label(self.dialog, text="Frame Rate:")
        self.frame_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)
        self.frame_entry = Entry(self.dialog)
        self.frame_entry.grid(row=2, column=1, padx=10, pady=5)

        self.format_label = Label(self.dialog, text="Output Format:")
        self.format_label.grid(row=3, column=0, padx=10, pady=5, sticky=W)
        self.format_var = StringVar(self.dialog)
        self.format_var.set("mp4")
        self.format_options = ["mp4", "h264p", "fhd", "hd", "dv", "mpg", "mpeg"]
        self.format_dropdown = OptionMenu(
            self.dialog, self.format_var, *self.format_options
        )
        self.format_dropdown.grid(row=3, column=1, padx=10, pady=5, sticky=W)

        self.progress_label = Label(self.dialog, text="Rendering Progress:")
        self.progress_label.grid(row=4, column=0, padx=10, pady=5, sticky=W)
        self.progress_scale = Scale(self.dialog, from_=0, to=100, orient=HORIZONTAL)
        self.progress_scale.grid(row=4, column=1, padx=10, pady=5, sticky=W)

        self.export_button = Button(self.dialog, text="Export", command=self.export)
        self.export_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def export(self):
        width = int(self.width_entry.get())
        height = int(self.height_entry.get())
        frame_rate = int(self.frame_entry.get())
        output_format = self.format_var.get()

        export_path = filedialog.asksaveasfilename(defaultextension=f".{output_format}")
        if export_path:
            # Perform export operation based on selected options
            # For demonstration, let's assume we're just showing a message box with export information
            messagebox.showinfo(
                "Export",
                f"Exporting video to: {export_path}\nWidth: {width}, Height: {height}, Frame Rate: {frame_rate}, Format: {output_format}",
            )

class AudioSettingsDialog:
    def __init__(self, parent):
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Audio Settings")

        # Volume Control
        self.volume_label = tk.Label(self.dialog, text="Volume:")
        self.volume_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.volume_scale = tk.Scale(self.dialog, from_=0, to=100, orient=tk.HORIZONTAL)
        self.volume_scale.set(50)  # Set default volume level
        self.volume_scale.grid(row=0, column=1, padx=10, pady=5)

        # Apply Button
        self.apply_button = tk.Button(self.dialog, text="Apply", command=self.apply_settings)
        self.apply_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def apply_settings(self):
        volume = self.volume_scale.get()
        messagebox.showinfo("Audio Settings Applied", f"Volume set to {volume}%")
class VideoEditorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("KR-Studio")

        # Get project name from command-line argument
        project_name = sys.argv[1] if len(sys.argv) > 1 else "Untitled"
        self.master.title(
            f"KR-Studio - {project_name}"
        )  # Set window title with project name

        # Variables
        self.project_name = None
        self.video_path = None
        self.cap = None
        self.video_canvas = None
        self.playing = False

        # Create Menus
        self.create_menus()

        # Video Preview Box
        self.video_preview_box = LabelFrame(
            self.master, text="Video Preview", padx=10, pady=10
        )
        self.video_preview_box.pack(padx=10, pady=10, fill=BOTH, expand=True)

        # Scrollbars
        self.x_scrollbar = Scrollbar(self.video_preview_box, orient=HORIZONTAL)
        self.x_scrollbar.pack(side=BOTTOM, fill=X)
        self.y_scrollbar = Scrollbar(self.video_preview_box)
        self.y_scrollbar.pack(side=RIGHT, fill=Y)

        self.video_canvas = Canvas(
            self.video_preview_box,
            xscrollcommand=self.x_scrollbar.set,
            yscrollcommand=self.y_scrollbar.set,
        )
        self.video_canvas.pack(fill=BOTH, expand=True)

        self.x_scrollbar.config(command=self.video_canvas.xview)
        self.y_scrollbar.config(command=self.video_canvas.yview)

        # Time and Audio Controls
        self.controls_frame = Frame(self.master)
        self.controls_frame.pack(padx=10, pady=10, fill=X)

        # Time Control
        self.time_label = Label(self.controls_frame, text="Video Frame Time:")
        self.time_label.pack(side=LEFT, padx=(0, 10))
        self.time_entry = Entry(self.controls_frame)
        self.time_entry.pack(side=LEFT)

        # Audio Control
        self.audio_label = Label(self.controls_frame, text="Audio:")
        self.audio_label.pack(side=LEFT, padx=(20, 10))
        self.audio_entry = Entry(self.controls_frame)
        self.audio_entry.pack(side=LEFT)

        # Video Preview Controls
        self.play_button = Button(
            self.controls_frame, text="Play", command=self.play_pause
        )
        self.play_button.pack(side=LEFT, padx=(20, 10))

        self.pause_button = Button(
            self.controls_frame, text="Pause", command=self.play_pause
        )
        self.pause_button.pack(side=LEFT, padx=(0, 10))

        self.jump_button = Button(
            self.controls_frame, text="Jump 5 sec", command=self.jump_5_sec
        )
        self.jump_button.pack(side=LEFT, padx=(0, 10))

        # Title Entry
        self.title_label = Label(self.controls_frame, text="Title:")
        self.title_label.pack(side=LEFT, padx=(20, 10))
        self.title_entry = Entry(self.controls_frame)
        self.title_entry.pack(side=LEFT)

        # Text Entry
        self.text_label = Label(self.controls_frame, text="Text:")
        self.text_label.pack(side=LEFT, padx=(20, 10))
        self.text_entry = Entry(self.controls_frame)
        self.text_entry.pack(side=LEFT)

        # Graphics Entry
        self.graphics_label = Label(self.controls_frame, text="Graphics:")
        self.graphics_label.pack(side=LEFT, padx=(20, 10))
        self.graphics_entry = Entry(self.controls_frame)
        self.graphics_entry.pack(side=LEFT)

        # Set window icon
        icon_path = "icon.ico"
        if os.path.exists(icon_path):
            self.master.iconbitmap(default=icon_path)

    def create_menus(self):
        # Menu Bar
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        # File Menu
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_video)
        file_menu.add_command(label="Open As", command=self.open_as)
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save_video)
        file_menu.add_command(label="Save As", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Import", command=self.import_video)
        file_menu.add_command(label="Export", command=self.export_video)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)
        file_menu.add_separator()
        file_menu.add_command(
            label="Show Recent Projects", command=self.show_recent_projects
        )
        menubar.add_cascade(label="File", menu=file_menu)

        # Edit Menu
        edit_menu = Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Screen")
        edit_menu.add_command(label="Effects")
        edit_menu.add_command(label="Time Out")
        edit_menu.add_command(label="Transitions")
        edit_menu.add_command(label="Noise")
        edit_menu.add_command(label="Audio Settings", command=self.open_audio_settings)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # Update Menu
        update_menu = Menu(menubar, tearoff=0)
        update_menu.add_command(label="Check for Updates")
        menubar.add_cascade(label="Update", menu=update_menu)

        # About Us Menu
        about_menu = Menu(menubar, tearoff=0)
        about_menu.add_command(label="About KR-Studio")
        menubar.add_cascade(label="About Us", menu=about_menu)

        # Help Menu
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="Help Contents", command=self.open_help_contents)
        help_menu.add_command(label="FAQ", command=self.open_faq)
        help_menu.add_separator()
        help_menu.add_command(label="Report Issue", command=self.report_issue)
        menubar.add_cascade(label="Help", menu=help_menu)

        # System Menu
        system_menu = Menu(menubar, tearoff=0)
        system_menu.add_command(label="System Preferences")
        system_menu.add_command(label="System Information")
        menubar.add_cascade(label="System", menu=system_menu)

    def open_video(self):
        self.video_path = filedialog.askopenfilename()
        if self.video_path:
            messagebox.showinfo("Success", f"Video opened: {self.video_path}")
            self.play_video()

    def open_as(self):
        file_path = filedialog.askopenfilename(filetypes=[("KR Studio Files", "*.kr")])
        if file_path:
            with open(file_path, "rb") as file:
                project_data = pickle.load(file)
                self.project_name = project_data.get("project_name")
                self.video_path = project_data.get("video_path")
            messagebox.showinfo("Success", f"Project '{self.project_name}' opened")

    def save_video(self):
        if self.video_path:
            project_data = {
                "project_name": self.project_name,
                "video_path": self.video_path,
            }
            with open(f"{self.project_name}.kr", "wb") as file:
                pickle.dump(project_data, file)
            messagebox.showinfo("Success", f"Project saved as {self.project_name}.kr")
        else:
            messagebox.showerror("Error", "No video loaded.")

    def save_as(self):
        project_data = {"project_name": "MyProject", "video_path": "/path/to/video"}

        save_path = filedialog.asksaveasfilename(defaultextension=".kr", filetypes=[("KR Studio Files", "*.kr")])

        if save_path:
            with open(save_path, "wb") as file:
                pickle.dump(project_data, file)
            messagebox.showinfo("Save Successful", f"Project saved as: {save_path}")
        else:
            messagebox.showwarning("Save Cancelled", "No file selected for saving.")


    def import_video(self):
        video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mkv")])

        if video_path:
            messagebox.showinfo("Import Successful", f"Video imported successfully: {video_path}")
        else:
            messagebox.showwarning("Import Cancelled", "No video file selected.")


    def export_video(self):
        self.export_dialog = ExportDialog(self.master)

    def play_video(self):
        if self.video_path:
            self.cap = cv2.VideoCapture(self.video_path)
            self.playing = True
            self.show_frame_with_title()

    def show_frame_with_title(self):
        ret, frame = self.cap.read()
        if ret and self.playing:
            frame = cv2.resize(frame, (720, 480))

            title = self.title_entry.get()
            if title:
                cv2.putText(
                    frame,
                    title,
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2,
                )

            # Overlay text on frame
            text = self.text_entry.get()
            if text:
                cv2.putText(
                    frame,
                    text,
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2,
                )

            # Overlay graphics on frame
            graphics = self.graphics_entry.get()
            if graphics:
                # Add code here to overlay graphics on frame
                pass

            # Convert frame to RGB and display
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            frame = ImageTk.PhotoImage(frame)
            self.video_canvas.create_image(0, 0, anchor=NW, image=frame)
            self.video_canvas.image = frame

            self.master.after(30, self.show_frame_with_title)
        else:
            self.cap.release()

    def exit_app(self):
        if self.cap:
            self.cap.release()
        self.master.destroy()
    
    def open_audio_settings(self):
      self.audio_settings_dialog = AudioSettingsDialog(self.master)

    def show_recent_projects(self):
        recent_projects = ["Project 1", "Project 2", "Project 3", "Project 4", "Project 5"]

        recent_projects_window = tk.Toplevel(self.master)
        recent_projects_window.title("Recent Projects")
        label_title = tk.Label(recent_projects_window, text="Recent Projects", font=("Helvetica", 14, "bold"))
        label_title.pack(pady=10)

        listbox_projects = tk.Listbox(recent_projects_window, width=50, height=10)
        listbox_projects.pack(padx=20, pady=10)
        for project in recent_projects:
            listbox_projects.insert(tk.END, project)


    def play_pause(self):
        self.playing = not self.playing

    def jump_5_sec(self):
        if self.cap:
            current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            jump_frame = current_frame + (5 * fps)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, jump_frame)
    def open_help_contents(self):
       webbrowser.open("https://example.com/help")

    def open_faq(self):
        webbrowser.open("https://example.com/faq")

    def report_issue(self):
        webbrowser.open("https://example.com/report_issue")

def main():
    root = Tk()
    app = VideoEditorApp(root)
    root.geometry("1080x600")
    root.mainloop()


if __name__ == "__main__":
    main()
