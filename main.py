from tkinter import *
import tkinter as tk
import time
import subprocess

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Main Window")
        
        self.label = tk.Label(self.master, text="KR-Video Editor", font=("Helvetica", 16))
        self.label.pack(pady=20)
        
        self.start_countdown(5)

    def start_countdown(self, seconds):
        self.master.after(seconds * 1000, self.run_video_editor)

    def run_video_editor(self):
        subprocess.run(["python", "video-editor.py"])
        self.master.destroy()

def main():
    root = tk.Tk()
    root.geometry("720x720")
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
