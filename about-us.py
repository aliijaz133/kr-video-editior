import tkinter as tk
from tkinter import filedialog
from tkinter import *
from datetime import datetime


class About_Us:
    def __init__(self, master):
        self.master = master
        self.master.title("KR-Studio - About Us")

        self.label = tk.Label(
            self.master, text="About Us", font=("Helvetica", 16, "bold")
        )
        self.label.pack(pady=10)

        self.text = tk.Text(self.master, wrap=WORD, width=60, height=15)
        self.text.pack(padx=20, pady=10)
        self.text.insert(tk.END, "About You:\n\n")
        self.text.insert(tk.END, "Hello! I am Ali ijaz, the creator of KR-Studio.\n")
        self.text.insert(
            tk.END,
            "I am passionate about video editing and developed KR-Studio to provide users with a powerful and intuitive tool for creating amazing videos.\n\n",
        )

        self.text.insert(tk.END, "About KR-Studio:\n\n")
        self.text.insert(
            tk.END,
            "KR-Studio is a versatile video editing software designed to meet the needs of both beginners and professionals.\n",
        )
        self.text.insert(
            tk.END,
            "With a wide range of features, including timeline editing, transition effects, keyframe animation, and more, KR-Studio offers everything you need to unleash your creativity.\n\n",
        )

        self.features_label = tk.Label(
            self.master, text="Key Features", font=("Helvetica", 14, "bold")
        )
        self.features_label.pack(pady=10)

        self.features_list = tk.Listbox(self.master, width=50, height=5)
        self.features_list.pack()
        features = [
            "Timeline editing",
            "Transition effects",
            "Keyframe animation",
            "Text and graphics overlay",
            "Export in multiple formats",
        ]
        for feature in features:
            self.features_list.insert(tk.END, feature)

        # Display current date and time
        self.datetime_label = tk.Label(
            self.master, text="Current Date and Time:", font=("Helvetica", 12)
        )
        self.datetime_label.pack(pady=10)

        self.current_datetime = tk.Label(
            self.master, text="", font=("Helvetica", 12, "italic")
        )
        self.current_datetime.pack()

        self.update_datetime()  # Update time initially
        self.master.after(1000, self.update_datetime)  # Update time every second

    def update_datetime(self):
        now = datetime.now()
        current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        self.current_datetime.config(text=current_datetime)
        self.master.after(
            1000, self.update_datetime
        )  # Schedule next update after 1 second


def main():
    root = tk.Tk()
    root.geometry("720x720")
    app = About_Us(root)
    root.mainloop()


if __name__ == "__main__":
    main()
