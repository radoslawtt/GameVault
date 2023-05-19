from custom_class import EventHandling
import tkinter as tk
from tkinter import messagebox
from tktooltip import ToolTip
import re
from database import replace_username


class ChangeUsername(tk.Toplevel):

    def __init__(self, parent, username):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.username = username
        self.title("Change username")
        self.geometry("250x120")
        self.resizable(False, False)
        self.config(bg="#6c6c6c")
        self.configure(highlightthickness=5, highlightcolor="#323232", highlightbackground="#323232")
        self.grid_columnconfigure(0, weight=1)

        self.new_username = tk.Entry(self, background="#a7a7a7", width=25, bd=5, font=("TkDefaultFont", 12))
        self.new_username.insert(0, "New username")
        self.new_username.bind("<FocusIn>", lambda event: EventHandling.remove_highlight(event), add="+")
        self.new_username.bind("<FocusIn>", lambda event: EventHandling.on_enter(event), add="+")
        self.new_username.bind("<FocusOut>", lambda event: EventHandling.on_leave(event, "CUW_new_username"))
        self.new_username.grid(row=0, column=0, padx=10, pady=10)

        ToolTip(self.new_username, msg="Usernames should begin with a capital letter and then use smaller letters. Usernames should be between three and nine characters long.")

        change_username = tk.Button(self, command=self.verify, text="Change username")
        change_username.config(bg="#a7a7a7", font=("TkDefaultFont", 12, "bold"),activebackground="#4f4f4f", relief="solid", borderwidth=3, cursor="hand2")
        change_username.bind("<Enter>", lambda event: EventHandling.button_hover(event, "#4f4f4f"))
        change_username.bind("<Leave>", lambda event: EventHandling.button_leave(event, "#a7a7a7"))
        change_username.grid(row=1, column=0, padx=20, pady=10)

    def verify(self):

        self.focus_set()
        new_username = self.new_username.get()
        validation = True
        regex = r"^[A-Z][a-z]{2,8}$"

        if not re.match(regex, new_username):
            self.new_username.config(highlightthickness=2, highlightbackground="red")
            validation = False
            messagebox.showerror("Error", "Username doesn't meet the requirements.")

        if validation:
            if replace_username(self.username, new_username):
                messagebox.showinfo("Info", "Successfully changed the username. Application will now close.")
                self.destroy()
                self.parent.destroy()
            else:
                messagebox.showerror("Error", "Username is already in use. Select another username.")