from custom_class import EventHandling
import tkinter as tk
from tkinter import messagebox
from tktooltip import ToolTip
import re
from database import replace_password


class ChangePassword(tk.Toplevel, EventHandling):

    def __init__(self, parent, username):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.username = username
        self.title("Change password")
        self.geometry("250x180")
        self.resizable(False, False)
        self.config(bg="#6c6c6c")
        self.configure(highlightthickness=5, highlightcolor="#323232", highlightbackground="#323232")
        self.grid_columnconfigure(0, weight=1)

        self.new_password = tk.Entry(self, background="#a7a7a7", width=25, bd=5, font=("TkDefaultFont", 12))
        self.new_password.insert(0, "New password")
        self.new_password.bind("<FocusIn>", lambda event: EventHandling.remove_highlight(event), add="+")
        self.new_password.bind("<FocusIn>", lambda event: EventHandling.on_enter(event), add="+")
        self.new_password.bind("<FocusOut>", lambda event: EventHandling.on_leave(event, "CPW_new_password"))
        self.new_password.grid(row=0, column=0, padx=10, pady=10)

        ToolTip(self.new_password, msg="At least one major letter and a number must be included in the password. Passwords should be between three and nine characters long.")


        self.cfm_new_password = tk.Entry(self, background="#a7a7a7", width=25, bd=5, font=("TkDefaultFont", 12), highlightcolor="red")
        self.cfm_new_password.insert(0, "Confirm new password")
        self.cfm_new_password.bind("<FocusIn>", lambda event: EventHandling.remove_highlight(event), add="+")
        self.cfm_new_password.bind("<FocusIn>", lambda event: EventHandling.on_enter(event), add="+")
        self.cfm_new_password.bind("<FocusOut>", lambda event: EventHandling.on_leave(event, "CPW_cfm_new_password"))
        self.cfm_new_password.grid(row=1, column=0, padx=10, pady=10)

        change_password = tk.Button(self, command=self.verify, text="Change password")
        change_password.config(bg="#a7a7a7", font=("TkDefaultFont", 12, "bold"),activebackground="#4f4f4f", relief="solid", borderwidth=3, cursor="hand2")
        change_password.bind("<Enter>", lambda event: EventHandling.button_hover(event, "#4f4f4f"))
        change_password.bind("<Leave>", lambda event: EventHandling.button_leave(event, "#a7a7a7"))
        change_password.grid(row=2, column=0, padx=20, pady=10)

    def verify(self):

        self.focus_set()
        new_password = self.new_password.get()
        regex = r"^(?=.*[A-Z])(?=.*\d)(?!.*[^\w]).{3,9}$"
        validation = True

        if not re.match(regex, new_password):
            validation = False
            self.new_password.config(highlightthickness=2, highlightbackground="red")
            messagebox.showerror("Error", "Password doesn't meet the requirements.")
        elif self.cfm_new_password.get() != new_password:
            validation = False
            self.cfm_new_password.config(highlightthickness=2, highlightbackground="red")
            messagebox.showerror("Error", "Passwords aren't the same.")

        if validation:
            replace_password(self.username, new_password)
            messagebox.showinfo("Info", "Successfully changed the password. Application will now close.")
            self.destroy()
            self.parent.destroy()