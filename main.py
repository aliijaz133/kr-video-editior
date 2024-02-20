import tkinter as tk
from PIL import Image, ImageTk
import subprocess

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("KR-Studio")
        
        self.label = tk.Label(self.master, text="KR-Studio", font=("Helvetica", 16))
        self.label.pack(pady=20)
        
        self.start_countdown(5)

        MainFrame = tk.Frame(self.master)
        MainFrame.pack(padx=10, pady=10)
        MainFrame.columnconfigure(0, weight=1)
        MainFrame.rowconfigure(0, weight=1)

        self.myImage = Image.open("/home/usamaumer/PycharmProjects/krVideoEditior/asset/icons/kr-video.png")
        self.photo = ImageTk.PhotoImage(self.myImage)
        self.image_label = tk.Label(MainFrame, image=self.photo)
        self.image_label.pack(padx=10, pady=10)

    def start_countdown(self, seconds):
        self.master.after(seconds * 1000, self.run_video_editor)

    def run_video_editor(self):
        subprocess.run(["python", "dashboard.py"])
        self.master.destroy()

def main():
    root = tk.Tk()
    root.geometry("720x720")
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
