from custom_class import EventHandling
import tkinter as tk
from tkinter import messagebox, ttk
from tktooltip import ToolTip
import re
from database import replace_security


class ChangeSecurity(tk.Toplevel):

    def __init__(self, parent, username):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.username = username
        self.title("Change username")
        self.geometry("350x150")
        self.resizable(False, False)
        self.config(bg="#6c6c6c")
        self.configure(highlightthickness=5, highlightcolor="#323232", highlightbackground="#323232")
        self.grid_columnconfigure(0, weight=1)

        combostyle = ttk.Style()

        if 'mcombostyle' not in ttk.Style().theme_names():
            combostyle.theme_create('mcombostyle', parent='alt',
                                     settings = {'TCombobox':
                                                 {'configure':
                                                  {'selectbackground': "#a7a7a7",
                                                    'selectforeground': "black",
                                                   'fieldbackground': "#a7a7a7",
                                                   'background': "#5e5e5e",

                                                   }}}
                                )
        combostyle.theme_use('mcombostyle')

        questions = [
            "What is the name of the town where you were born?",
            "What was your favorite subject in high school?",
            "What was your first car?",
            "What is the name of the road you grew up on?",
            "What is the name of your first pet?",
            "What elementary school did you attend?"
        ]

        self.new_question = ttk.Combobox(self, style="TCombobox", values=questions, state="readonly", takefocus=True, width=44, font=("TkDefaultFont", 10))
        self.new_question.grid(row=0, column=0)
        self.new_question.current(0)
        self.option_add("*TCombobox*Listbox.Background", "#a7a7a7")
        self.option_add("*TCombobox*Listbox.selectBackground", "#5e5e5e")
        self.option_add('*TCombobox*Listbox.selectForeground', "black")

        self.new_answer = tk.Entry(self, background="#a7a7a7", width=25, bd=5, font=("TkDefaultFont", 12))
        self.new_answer.insert(0, "New answer")
        self.new_answer.bind("<FocusIn>", lambda  event: EventHandling.remove_highlight(event), add="+")
        self.new_answer.bind("<FocusIn>", lambda event: EventHandling.on_enter(event), add="+")
        self.new_answer.bind("<FocusOut>", lambda event: EventHandling.on_leave(event, "CSW_new_answer"))
        self.new_answer.grid(row=1, column=0, padx=10, pady=10)

        ToolTip(self.new_answer, msg="Answer contain only letters. Answer should be between three and nine characters long.")

        change_security = tk.Button(self, command=self.verify, text="Change security")
        change_security.config(bg="#a7a7a7", font=("TkDefaultFont", 12, "bold"),activebackground="#4f4f4f", relief="solid", borderwidth=3, cursor="hand2")
        change_security.bind("<Enter>", lambda event: EventHandling.button_hover(event, "#4f4f4f"))
        change_security.bind("<Leave>", lambda event: EventHandling.button_hover(event, "#a7a7a7"))
        change_security.grid(row=2, column=0, padx=20, pady=10)

    def verify(self):

        self.focus_set()
        new_answer = self.new_answer.get()
        new_question = self.new_question.get()
        validation = True
        regex = r"^[a-zA-Z]{3,9}$"

        if not re.match(regex, new_answer):
            self.new_answer.config(highlightthickness=2, highlightbackground="red")
            validation = False
            messagebox.showerror("Error", "Answer doesn't meet the requirements.")

        if validation:
            replace_security(self.username, new_question, new_answer)
            messagebox.showinfo("Info", "Successfully changed the security. Application will now close.")
            self.destroy()
            self.parent.destroy()