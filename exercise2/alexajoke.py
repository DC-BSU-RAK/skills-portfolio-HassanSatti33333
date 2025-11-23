import tkinter as tk
from tkinter import font, messagebox, PhotoImage
import random
import os


class JokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Joke App")
        self.root.geometry("500x550")
        self.root.config(bg="white")

        #laoding jokes from file
        try:
            with open("resources/randomJokes.txt", "r", encoding="utf-8") as f:
                self.jokes = []
                for line in f:
                    line = line.strip()
                    if line and "?" in line:
                        setup, punchline = line.split("?", 1)
                        self.jokes.append({"setup": setup + "?", "punchline": punchline.strip()})
        except FileNotFoundError:
            messagebox.showerror("Make sure file is in proper place")
            self.jokes = []

        self.current_joke = None

        try:
            self.title_font = font.Font(family="Jokerman", size=40, weight="bold")
        except:
            self.title_font = font.Font(size=40, weight="bold")

        self.box_font = font.Font(size=14)
        self.button_font = font.Font(size=14, weight="bold")

        self.main_canvas = tk.Canvas(root, bg="white", highlightthickness=0)
        self.main_canvas.pack(fill="both", expand=True)

        self.center_frame = tk.Frame(self.main_canvas, bg="white")
        self.main_canvas.create_window(0.5, 0.5, window=self.center_frame, anchor="center", tags="center_frame")

        self.title_label = tk.Label(self.center_frame, text="Joke App", font=self.title_font, bg="white")
        self.title_label.pack(pady=10)

        self.joke_var = tk.StringVar(value="Joke box")
        self.joke_label = tk.Label(self.center_frame, textvariable=self.joke_var,
                                   font=self.box_font, bg="#d3d3d3",
                                   width=40, height=2, relief="solid", anchor="w", padx=10)
        self.joke_label.pack(pady=10)

        self.punchline_var = tk.StringVar(value="Punchline box")
        self.punchline_label = tk.Label(self.center_frame, textvariable=self.punchline_var,
                                        font=self.box_font, bg="#d3d3d3",
                                        width=40, height=2, relief="solid", anchor="w", padx=10)
        self.punchline_label.pack(pady=10)

        self.button_frame = tk.Frame(self.center_frame, bg="white")
        self.button_frame.pack(pady=20)

        button_opts = {
            "bg": "yellow",
            "fg": "purple",
            "font": self.button_font,
            "width": 25,
            "height": 1,
            "cursor": "hand2",
        }

        self.btn_tell_joke = tk.Button(self.button_frame, text="Alexa tell me a joke", command=self.tell_joke, **button_opts)
        self.btn_next_joke = tk.Button(self.button_frame, text="Next Joke", command=self.next_joke, **button_opts)
        self.btn_reveal_punchline = tk.Button(self.button_frame, text="Reveal Punchline", command=self.reveal_punchline, **button_opts)
        self.btn_quit = tk.Button(self.button_frame, text="Quit", command=root.quit, **button_opts)

        self.btn_tell_joke.pack(pady=5)
        self.btn_next_joke.pack(pady=5)
        self.btn_reveal_punchline.pack(pady=5)
        self.btn_quit.pack(pady=5)

        laugh_path = "resources/laughing.png"
        if os.path.exists(laugh_path):
            self.laugh_img = PhotoImage(file=laugh_path)
        else:
            self.laugh_img = None
            messagebox.showwarning("Warning", "Laughing image not found.")

        self.laughing_faces = []

        self.main_canvas.bind("<Configure>", self.center_content)

    def center_content(self, event):
        """Keep the inner frame centered when window resizes"""
        self.main_canvas.coords("center_frame", event.width / 2, event.height / 2)

    def tell_joke(self):
        if not self.jokes:
            messagebox.showinfo("Info", "No jokes loaded.")
            return
        self.current_joke = random.choice(self.jokes)
        self.joke_var.set(self.current_joke["setup"])
        self.punchline_var.set("Punchline box")

    def next_joke(self):
        if not self.current_joke:
            self.tell_joke()
            return

        idx = self.jokes.index(self.current_joke)
        self.current_joke = self.jokes[(idx + 1) % len(self.jokes)]
        self.joke_var.set(self.current_joke["setup"])
        self.punchline_var.set("Punchline box")

    def reveal_punchline(self):
        if not self.current_joke:
            messagebox.showinfo("Info", "Tell a joke first.")
            return

        self.punchline_var.set(self.current_joke["punchline"])

        if self.laugh_img:
            w = self.main_canvas.winfo_width()
            h = self.main_canvas.winfo_height()

            x = random.randint(0, max(0, w - self.laugh_img.width()))
            y = random.randint(0, max(0, h - self.laugh_img.height()))

            img_id = self.main_canvas.create_image(x, y, anchor="nw", image=self.laugh_img)
            self.laughing_faces.append(img_id)
if __name__ == "__main__":
    root = tk.Tk()
    app = JokeApp(root)
    root.mainloop()
