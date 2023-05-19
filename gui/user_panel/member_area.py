import tkinter as tk
from custom_class import EventHandling
from gui.user_panel.toplevel_windows.change_username import ChangeUsername
from gui.user_panel.toplevel_windows.change_password import ChangePassword
from gui.user_panel.toplevel_windows.change_security import ChangeSecurity
from gui.user_panel.toplevel_windows.delete_account import DeleteAccount
from games import tetris, snake, sudoku, hangman
import sys
from tkinter import ttk
from database import load_ranking


class MemberArea(tk.Tk):

    def __init__(self, username):
        tk.Tk.__init__(self)
        self.username = username
        self.title("Member Area")
        self.geometry("600x600")
        self.resizable(False, False)
        self.window = self
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._init_buttons_frame()
        self.frame_container = tk.Frame(self, bg="red")
        self.frame_container.grid(row=1, column=0, sticky="news")
        self.frame_container.grid_columnconfigure(0, weight=1)
        self.frame_container.grid_rowconfigure(0, weight=1)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.frames = [AccountFrame(self, self.frame_container, self.username), GameFrame(self.frame_container, self.username, self.window)]

    def on_closing(self):
        sys.exit()

    def _init_buttons_frame(self):

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.config(highlightthickness=5, highlightcolor="#323232", highlightbackground="#323232", height=50)
        self.buttons_frame.grid_propagate(False)

        self.buttons_frame.grid_rowconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(1, weight=1)

        self.buttons_frame.config(bg="black")
        self.buttons_frame.grid(row=0, column=0, sticky="news")

        self.games_label = tk.Label(self.buttons_frame, width=15, text="Games")
        self.games_label.config(justify='center', background="#a7a7a7", font=("TkDefaultFont", 12, "bold"), cursor="hand2", bd=2, relief="solid", highlightcolor="#323232")
        self.games_label.bind("<Enter>", lambda event: EventHandling.button_hover(event, "#4f4f4f"))
        self.games_label.bind("<Leave>", lambda event: EventHandling.button_leave(event, "#a7a7a7"))
        self.games_label.bind("<Button-1>", self.game_frame)
        self.games_label.grid(row=0, column=0, sticky="news")

        account_label = tk.Label(self.buttons_frame, width=15, text="Account")
        account_label.config(justify='center', background="#a7a7a7", font=("TkDefaultFont", 12, "bold"),
                                  cursor="hand2", bd=2, relief="solid", highlightcolor="#323232")
        account_label.bind("<Enter>", lambda event: EventHandling.button_hover(event, "#4f4f4f"))
        account_label.bind("<Leave>", lambda event: EventHandling.button_leave(event, "#a7a7a7"))
        account_label.bind("<Button-1>", self.account_frame)
        account_label.grid(row=0, column=1, sticky="news")

    def game_frame(self, event):
        self.frames[1].tkraise()

    def account_frame(self, event):
        self.frames[0].tkraise()

class AccountFrame(tk.Frame):

    def __init__(self, master, box, username):
        tk.Frame.__init__(self, box)

        self.master = master
        self.username = username
        self.config(highlightthickness=15, highlightcolor="#323232", highlightbackground="#323232", background="#6c6c6c")
        self.grid(row=0, column=0, sticky="news")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        username = tk.Button(self, width=20, text="Change username", command=self.change_username)
        username.config(bg="#a7a7a7", font=("TkDefaultFont", 10, "bold"), activebackground="#4f4f4f", relief="solid",
                        borderwidth=3, cursor="hand2")
        username.bind("<Enter>", lambda event: EventHandling.button_hover(event, "#4f4f4f"))
        username.bind("<Leave>", lambda event: EventHandling.button_leave(event, "#a7a7a7"))
        username.grid(row=0, column=0, padx=20, pady=20)

        password = tk.Button(self, width=20, text="Change password", command=self.change_password)
        password.config(bg="#a7a7a7", font=("TkDefaultFont", 10, "bold"), activebackground="#4f4f4f", relief="solid",
                        borderwidth=3, cursor="hand2")
        password.bind("<Enter>", lambda event: EventHandling.button_hover(event, "#4f4f4f"))
        password.bind("<Leave>", lambda event: EventHandling.button_leave(event, "#a7a7a7"))
        password.grid(row=0, column=1, padx=20, pady=20)

        security_question = tk.Button(self, width=20, text="Change security question",
                                      command=self.change_security)
        security_question.config(bg="#a7a7a7", font=("TkDefaultFont", 10, "bold"), activebackground="#4f4f4f",
                                 relief="solid", borderwidth=3, cursor="hand2")
        security_question.bind("<Enter>", lambda event: EventHandling.button_hover(event, "#4f4f4f"))
        security_question.bind("<Leave>", lambda event: EventHandling.button_leave(event, "#a7a7a7"))
        security_question.grid(row=1, column=0, padx=20, pady=20)

        delete_account_button= tk.Button(self, width=20, text="Delete account", command=self.delete_account)
        delete_account_button.config(bg="#a7a7a7", font=("TkDefaultFont", 10, "bold"), activebackground="#4f4f4f", relief="solid",
                        borderwidth=3, cursor="hand2")
        delete_account_button.bind("<Enter>", lambda event: EventHandling.button_hover(event, "#4f4f4f"))
        delete_account_button.bind("<Leave>", lambda event: EventHandling.button_leave(event, "#a7a7a7"))
        delete_account_button.grid(row=1, column=1, padx=20, pady=20)


    def change_password(self):
        ChangePassword(self.master, self.username).grab_set()

    def change_username(self):
        ChangeUsername(self.master, self.username).grab_set()

    def change_security(self):
        ChangeSecurity(self.master, self.username).grab_set()

    def delete_account(self):
        DeleteAccount(self.master, self.username).grab_set()



class GameFrame(tk.Frame):
    def __init__(self, box, username, window):
        tk.Frame.__init__(self, box)

        self.window = window
        self.username = username
        self.box= box

        # FRAME
        self.config(highlightthickness=15, highlightcolor="#323232", highlightbackground="#323232", background="#6c6c6c")
        self.grid(row=0, column=0, sticky="news")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=2)

        # SNAKE
        snake_label = tk.Label(self, text="Snake", background="#6c6c6c", foreground="#282828",
                               font=("TkDefaultFont", 15, "bold"))
        snake_label.grid(row=0, column=0)

        self.snake_icon = tk.PhotoImage(file="resources/gui_assets/images/snake_icon.png")
        snake_button = tk.Button(self, image=self.snake_icon, command=self.open_snake)
        snake_button.config(background="#6c6c6c", borderwidth=0, activebackground="#6c6c6c", cursor="hand2")
        snake_button.grid(row=1, column=0, sticky="n")

        # SUDOKU
        sudoku_label = tk.Label(self, text="Sudoku", background="#6c6c6c", foreground="#282828",
                                font=("TkDefaultFont", 15, "bold"))
        sudoku_label.grid(row=0, column=1)

        self.sudoku_icon = tk.PhotoImage(file="resources/gui_assets/images/sudoku_icon.png")
        sudoku_button = tk.Button(self, image=self.sudoku_icon, command=self.open_sudoku)
        sudoku_button.config(background="#6c6c6c", borderwidth=0, activebackground="#6c6c6c", cursor="hand2")
        sudoku_button.grid(row=1, column=1, sticky="n")

        # HANGMAN
        hangman_label = tk.Label(self, text="Hangman", background="#6c6c6c", foreground="#282828",
                                font=("TkDefaultFont", 15, "bold"))
        hangman_label.grid(row=2, column=0)

        self.hangman_icon = tk.PhotoImage(file="resources/gui_assets/images/hangman_icon.png")
        hangman_button = tk.Button(self, image=self.hangman_icon, command=self.open_hangman)
        hangman_button.config(background="#6c6c6c", borderwidth=0, activebackground="#6c6c6c", cursor="hand2")
        hangman_button.grid(row=3, column=0, sticky="n")

        # TETRIS
        tetris_label = tk.Label(self, text="Tetris", background="#6c6c6c", foreground="#282828", font=("TkDefaultFont", 15, "bold"))
        tetris_label.grid(row=2, column=1)
        self.tetris_icon = tk.PhotoImage(file="resources/gui_assets/images/tetris_icon.png")
        tetris_button = tk.Button(self, image=self.tetris_icon, command=self.open_tetris)
        tetris_button.config(background="#6c6c6c", borderwidth=0, activebackground="#6c6c6c", cursor="hand2")
        tetris_button.grid(row=3, column=1, sticky="n")

    def open_tetris(self):
        self.window.withdraw()
        tetris.start_game(self.username, self.window)

    def open_sudoku(self):
        self.window.withdraw()
        sudoku.start_game(self.username, self.window)

    def open_snake(self):
        self.window.withdraw()
        snake.start_game(self.username, self.window)

    def open_hangman(self):
        self.window.withdraw()
        hangman.start_game(self.username, self.window)






