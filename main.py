import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import subprocess


class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("KR-Studio")

        self.label = tk.Label(self.master, text="KR-Studio", font=("Helvetica", 16))
        self.label.pack(pady=20)

        MainFrame = tk.Frame(self.master)
        MainFrame.pack(padx=10, pady=10)
        MainFrame.columnconfigure(0, weight=1)
        MainFrame.rowconfigure(0, weight=1)

        self.myImage = Image.open("./asset/icons/kr-video.png")
        self.photo = ImageTk.PhotoImage(self.myImage)
        self.image_label = tk.Label(MainFrame, image=self.photo)
        self.image_label.pack(padx=10, pady=10)

        self.spinner_canvas = tk.Canvas(master, width=200, height=200)
        self.spinner_canvas.pack(pady=10)

        self.spinner_image = Image.open("./asset/images/spinner.gif")
        self.spinner_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(self.spinner_image)]
        self.spinner_index = 0
        self.spinner_animation()

        self.start_countdown(5)

    def start_countdown(self, seconds):
        self.master.after(seconds * 1000, self.switch_to_dashboard)

    def switch_to_dashboard(self):
        self.master.destroy()
        subprocess.Popen(["python", "dashboard.py"])

    def spinner_animation(self):
        self.spinner_canvas.delete("all")
        self.spinner_canvas.create_image(100, 100, image=self.spinner_frames[self.spinner_index])
        self.spinner_index += 1
        if self.spinner_index >= len(self.spinner_frames):
            self.spinner_index = 0
        self.master.after(100, self.spinner_animation)


def main():
    root = tk.Tk()
    root.geometry("720x720")
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
