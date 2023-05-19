import tkinter as tk
from tkinter import ttk, messagebox
from database import register_user
from custom_class import EventHandling
from tktooltip import ToolTip
import re

# Creating window
class RegisterWindow(tk.Toplevel):

    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("Registration")
        self.geometry("498x498")
        self.resizable(False, False)
        self.config(bg="#6c6c6c")
        self.configure(highlightthickness=15, highlightcolor="#323232", highlightbackground="#323232")

        vcmd = (self.register(self.validate), '%P')

        #Username
        self.reg_username_label = tk.Label(self, width=10, text="Username")
        self.reg_username_label.config(background="#6c6c6c", fg="#282828", font=("TkDefaultFont", 12, "bold"), anchor=tk.W)
        self.reg_username_label.place(x=95, y=25)

        self.reg_username_entry = tk.Entry(self, validate='key', validatecommand=vcmd)
        self.reg_username_entry.config(width=30, bd=5, font=("TkDefaultFont", 12 ), bg="#a7a7a7")
        self.reg_username_entry.bind("<FocusIn>", lambda event: EventHandling.remove_highlight(event))
        self.reg_username_entry.place(x=100, y=50)

        ToolTip(self.reg_username_entry,msg="Usernames should begin with a capital letter and then use smaller letters. Usernames should be between three and nine characters long.")

        #Password
        self.reg_password_label = tk.Label(self, width=15, text="Password")
        self.reg_password_label.config(background="#6c6c6c", fg="#282828", font=("TkDefaultFont", 12, "bold"), anchor=tk.W)
        self.reg_password_label.place(x=96, y=90)

        self.reg_password = tk.Entry(self, validate='key', validatecommand=vcmd, show="*")
        self.reg_password.config(width=30, bd=5, font=("TkDefaultFont", 12, ), bg="#a7a7a7")
        self.reg_password.bind("<FocusIn>", lambda event: EventHandling.remove_highlight(event))
        self.reg_password.place(x=100, y=115)

        ToolTip(self.reg_password,msg="At least one major letter and a number must be included in the password. Passwords should be between three and nine characters long.")

        self.reg_cfn_password_label = tk.Label(self, width=15, text="Confirm password")
        self.reg_cfn_password_label.config(background="#6c6c6c", fg="#282828", font=("TkDefaultFont", 12, "bold"))
        self.reg_cfn_password_label.place(x=92, y=155)

        self.reg_password_confirm = tk.Entry(self, validate='key', validatecommand=vcmd, show="*")
        self.reg_password_confirm.config(width=30, bd=5, font=("TkDefaultFont", 12, ), bg="#a7a7a7")
        self.reg_password_confirm.bind("<FocusIn>", lambda event: EventHandling.remove_highlight(event))
        self.reg_password_confirm.place(x=100, y=180)


        # Display help questions
        questions = [
            "What is the name of the town where you were born?",
            "What was your favorite subject in high school?",
            "What was your first car?",
            "What is the name of the road you grew up on?",
            "What is the name of your first pet?",
            "What elementary school did you attend?"
        ]

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

        self.reg_question_box_label = tk.Label(self, width=25, text="In case you forgot your password")
        self.reg_question_box_label.config(background="#6c6c6c", fg="#282828", font=("TkDefaultFont", 12, "bold"))
        self.reg_question_box_label.place(x=100, y=220)

        self.reg_question_box = ttk.Combobox(self, style="TCombobox",values=questions, state="readonly", takefocus=True, width=44, font=("TkDefaultFont", 8))
        self.reg_question_box.place(x=100, y=240)
        self.reg_question_box.current(0)
        self.option_add("*TCombobox*Listbox.Background", "#a7a7a7")
        self.option_add("*TCombobox*Listbox.selectBackground", "#5e5e5e")
        self.option_add('*TCombobox*Listbox.selectForeground', "black")



        # Display anserw
        self.reg_answer_label = tk.Label(self, width=25, text="Answer to selected question")
        self.reg_answer_label.config(background="#6c6c6c", fg="#282828", font=("TkDefaultFont", 12, "bold"))
        self.reg_answer_label.place(x=80, y=265)


        self.reg_answer_entry = tk.Entry(self, validate='key', validatecommand=vcmd)
        self.reg_answer_entry.config(width=30, bd=5, font=("TkDefaultFont", 12, ), bg="#a7a7a7")
        self.reg_answer_entry.bind("<FocusIn>", lambda event: EventHandling.remove_highlight(event))
        self.reg_answer_entry.place(x=100, y=290)

        ToolTip(self.reg_answer_entry,msg="Answer contain only letters. Answer should be between three and nine characters long.")

        # Display registation button
        self.reg_button = tk.Button(self,width=20, text="Register",command=self.reg_verification)
        self.reg_button.config(bg="#a7a7a7", font=("TkDefaultFont", 12, "bold"),activebackground="#4f4f4f", relief="solid", borderwidth=3, cursor="hand2")
        self.reg_button.place(x=135, y=360)
        self.reg_button.bind("<Enter>", lambda event: EventHandling.button_hover(event, "#4f4f4f"))
        self.reg_button.bind("<Leave>", lambda event: EventHandling.button_leave(event, "#a7a7a7"))
        self.reg_button.bind("<Button-1>", lambda event: EventHandling.window_focus(self))

    #Username
    def validate(self, value):
        if len(value) <= 9:
            return True
        else:
            return False

    def reg_verification(self):

        username = self.reg_username_entry.get()
        password = self.reg_password.get()
        answer = self.reg_answer_entry.get()
        validation = True
        username_regex = r"^[A-Z][a-z]{2,8}$"
        password_regex = r"^(?=.*[A-Z])(?=.*\d)(?!.*[^\w]).{3,9}$"
        answer_regex = r"^[a-zA-Z]{3,9}$"

        if not re.match(username_regex, username):
            self.reg_username_entry.config(highlightthickness=2, highlightbackground='red')
            validation = False

        if not re.match(password_regex, password):
            self.reg_password.config(highlightthickness=2, highlightbackground='red')
            validation = False

        if self.reg_password_confirm.get() != password:
            self.reg_password_confirm.config(highlightthickness=2, highlightbackground='red')
            validation = False

        if not re.match(answer_regex, answer):
            self.reg_answer_entry.config(highlightthickness=2, highlightbackground='red')
            validation = False

        if not validation:
            messagebox.showwarning("Error", "Incorrect data was entered")
        else:
            register_user(username, password, self.reg_question_box.get(), answer)
            messagebox.showinfo("Success", "Your account has been register, You can sign in now.")
            self.destroy()

