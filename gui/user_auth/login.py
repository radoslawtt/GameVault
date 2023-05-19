import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from database import login_user
from gui.user_panel.member_area import MemberArea
from gui.user_auth.toplevel_windows.registration import RegisterWindow
from gui.user_auth.toplevel_windows.forgot_password import ForgotPasswordWindow
from custom_class import EventHandling


class LoginWindow(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Login")
        self.geometry("498x498")
        self.resizable(False, False)
        self.gif_label = tk.Label(self)
        self.gif_label.pack(fill=tk.BOTH)

        self.frame_id = None
        self.gif_frames = []
        self.frame_delay = 0
        self.frame_count = -1
        self.current_frame = None

        self.start_background()

        self.canvas = tk.Canvas(self, width=300, height=300, bg="#0E0E0E", highlightthickness=1, highlightbackground="grey")
        self.canvas.create_line(75, 205, 140, 205, fill="grey", width=1)
        self.canvas.create_line(160, 205, 225, 205, fill="grey", width=1)
        self.text = self.canvas.create_text(150, 204, text="or", fill="#848484")
        self.canvas.bind("<Button-1>", lambda event: EventHandling.window_focus(self.canvas))
        self.canvas.place(x=100, y=100)

        self.username_entry = tk.Entry(self, width=20, bd=5, font=("TkDefaultFont", 13))
        self.username_entry.config(bg="#848484")
        self.username_entry.insert(0, "Username...")
        self.username_entry.bind("<FocusIn>", lambda event: EventHandling.on_enter(event), add="+")
        self.username_entry.bind("<FocusIn>", lambda event: EventHandling.remove_highlight(event), add="+")
        self.username_entry.bind("<FocusOut>", lambda event: EventHandling.on_leave(event, "LW_username_entry"))
        self.canvas.create_window(150, 60, window=self.username_entry)

        self.password_entry = tk.Entry(self, width=20, bd=5, font=("TkDefaultFont", 13))
        self.password_entry.config(bg="#848484")
        self.password_entry.insert(0, "Password...")
        self.password_entry.bind("<FocusIn>", lambda event: EventHandling.on_enter(event), add="+")
        self.password_entry.bind("<FocusIn>", lambda event: EventHandling.remove_highlight(event), add="+")
        self.password_entry.bind("<FocusOut>", lambda event: EventHandling.on_leave(event, "LW_password_entry"))
        self.canvas.create_window(150, 105, window=self.password_entry)

        self.login_button = tk.Button(self, width=20, text="Login", bg="#848484", bd=5, activebackground="#5e5e5e", command=self.login_verify, cursor="hand2")
        self.login_button.bind("<Enter>", lambda event: EventHandling.button_hover(event, "#5e5e5e"))
        self.login_button.bind("<Leave>", lambda event: EventHandling.button_hover(event, "#848484"))
        self.canvas.create_window(150, 180, window=self.login_button)

        self.register_button = tk.Button(self, width=20, text="Register", bd=5, activebackground="#5e5e5e", command=self.open_register_window, cursor="hand2")
        self.register_button.config(bg="#848484")
        self.register_button.bind("<Enter>", lambda event: EventHandling.button_hover(event, "#5e5e5e"))
        self.register_button.bind("<Leave>", lambda event: EventHandling.button_hover(event, "#848484"))
        self.canvas.create_window(150, 235, window=self.register_button)

        self.text = self.canvas.create_text(200, 135, text="Forgot password?", fill="#848484")
        self.canvas.tag_bind(self.text, "<Button-1>", lambda event: self.open_forgot_password_window())
        self.canvas.tag_bind(self.text, "<Enter>", lambda event: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind(self.text, "<Leave>", lambda event: self.canvas.config(cursor=""))

    def start_background(self):

        def prepare_gif():

            # Load GIF and create frames
            background_gif = Image.open("resources/gui_assets/images/login_background.gif")
            for i in range(0, background_gif.n_frames):
                background_gif.seek(i)
                self.gif_frames.append(background_gif.copy())

            # Set delay between frames
            self.frame_delay = background_gif.info['duration']

            play_gif()

        def play_gif():

            if self.frame_count >= len(self.gif_frames) - 1:
                self.frame_count = -1

            self.frame_count += 1
            self.current_frame = ImageTk.PhotoImage(self.gif_frames[self.frame_count])
            self.gif_label.config(image=self.current_frame)
            self.frame_id = self.after(self.frame_delay, play_gif)

        prepare_gif()

    def open_register_window(self):
        RegisterWindow(self).grab_set()

    def open_forgot_password_window(self):
        ForgotPasswordWindow(self).grab_set()

    def login_verify(self):

        username = self.username_entry.get()

        validation = login_user(username, self.password_entry.get())

        if validation:
            self.after_cancel(self.frame_id)
            self.destroy()
            MemberArea(username).mainloop()
        else:
            self.username_entry.config(highlightthickness=2, highlightbackground='red')
            self.password_entry.config(highlightthickness=2, highlightbackground='red')
            messagebox.showerror("Error", "We don't have matching data in our database")

