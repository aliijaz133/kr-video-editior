from tkinter import *
import tkinter as tk
from tkinter import filedialog
import cv2

class VideoEditorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("KR-Studio")

        self.video_frames = []

        self.create_widgets()

    def create_widgets(self):
        self.select_video_button = tk.Button(self.master, text="Select Video", command=self.select_video)
        self.select_video_button.pack()

        self.play_button = tk.Button(self.master, text="Play", command=self.play_video)
        self.play_button.pack()

        self.stop_button = tk.Button(self.master, text="Stop", command=self.stop_video)
        self.stop_button.pack()

    def select_video(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.video_frames = self.extract_frames(file_path)

    def extract_frames(self, video_path):
        video_frames = []
        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                video_frames.append(frame)
            else:
                break
        cap.release()
        return video_frames

    def play_video(self):
        for frame in self.video_frames:
            cv2.imshow('Video', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

    def stop_video(self):
        cv2.destroyAllWindows()

def main():
    root = tk.Tk()
    app = VideoEditorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
