from custom_class import EventHandling
import tkinter as tk
from tkinter import messagebox
from database import delete_account


class DeleteAccount(tk.Toplevel):

    def __init__(self, parent, username):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.username = username
        self.title("Delete account")
        self.geometry("350x120")
        self.resizable(False, False)
        self.config(bg="#6c6c6c")
        self.configure(highlightthickness=5, highlightcolor="#323232", highlightbackground="#323232")
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.question = tk.Label(self, text="Are you sure you want to delete your account?", font=("TkDefaultFont", 12), bg="#6c6c6c")
        self.question.grid(row=0, columnspan=2)

        self.yes_button = tk.Button(self, command=self.delete_account, text="Yes")
        self.yes_button.config(bg="#a7a7a7", font=("TkDefaultFont", 12, "bold"), activebackground="#4f4f4f", relief="solid", borderwidth=3, cursor="hand2", justify="center")
        self.yes_button.bind("<Enter>", lambda event: EventHandling.button_hover(event, "#4f4f4f"))
        self.yes_button.bind("<Leave>", lambda event: EventHandling.button_leave(event, "#a7a7a7"))
        self.yes_button.grid(row=1, column=0)

        self.no_button = tk.Button(self, command=self.close_window, text="No")
        self.no_button.config(bg="#a7a7a7", font=("TkDefaultFont", 12, "bold"), activebackground="#4f4f4f", relief="solid", borderwidth=3, cursor="hand2", justify="center")
        self.no_button.bind("<Enter>", lambda event: EventHandling.button_hover(event, "#4f4f4f"))
        self.no_button.bind("<Leave>", lambda event: EventHandling.button_leave(event, "#a7a7a7"))
        self.no_button.grid(row=1, column=1)

    def close_window(self):
        self.destroy()

    def delete_account(self):
        delete_account(self.username)
        messagebox.showinfo("Success", "Account deleted successfully.")
        self.destroy()
        self.parent.destroy()