import tkinter as tk
from tkinter import messagebox
from database import username_exist, answer_verification, replace_password
from custom_class import EventHandling
import re
from tktooltip import ToolTip


class ForgotPasswordWindow(tk.Toplevel):

    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("Password reset")
        self.geometry("498x498")
        self.resizable(False, False)
        self.config(bg="#6c6c6c")
        self.configure(highlightthickness=15, highlightcolor="#323232", highlightbackground="#323232")

        self._init_layout()

    def _init_layout(self):

        self.vcmd = (self.register(self.validate), '%P')
        # Username
        self.username_label = tk.Label(self, width=10, text="Username")
        self.username_label.config(background="#6c6c6c", fg="#282828", font=("TkDefaultFont", 12, "bold"), anchor=tk.W)
        self.username_label.place(x=95, y=25)

        self.username_entry = tk.Entry(self, validate='key', validatecommand=self.vcmd)
        self.username_entry.config(width=30, bd=5, font=("TkDefaultFont", 12,), bg="#a7a7a7")
        self.username_entry.bind("<FocusIn>", lambda event: EventHandling.remove_highlight(event))
        self.username_entry.place(x=100, y=50)

        self.continue_button = tk.Button(self, width=20, text="Continue",command=self.username_verification)
        self.continue_button.config(bg="#a7a7a7", font=("TkDefaultFont", 12, "bold"), activebackground="#4f4f4f", relief="solid",borderwidth=3, cursor="hand2")
        self.continue_button.place(x=135, y=120)
        self.continue_button.bind("<Enter>", lambda event: EventHandling.button_hover(event, "#4f4f4f"))
        self.continue_button.bind("<Leave>", lambda event: EventHandling.button_hover(event, "#a7a7a7"))
        self.continue_button.bind("<Button-1>", lambda event: EventHandling.window_focus(self))

    def _init_layout2(self):

        self.continue_button.place_forget()
        self.username_entry.config(state="disabled",)

        self.text_formula = tk.Label(self, width=35, text="Please answer your security question.")
        self.text_formula.config(background="#6c6c6c", fg="#282828", font=("TkDefaultFont", 12, "bold"), anchor=tk.W)
        self.text_formula.place(x=95, y=85)

        self.help_question = tk.Label(self, width=45, text="{}".format(self.question))
        self.help_question.config(background="#6c6c6c", fg="#282828", font=("TkDefaultFont", 10, ), anchor=tk.W)
        self.help_question.place(x=95, y=105)

        self.answer_entry = tk.Entry(self, validate='key', validatecommand= self.vcmd)
        self.answer_entry.configure(width=30, bd=5, font=("TkDefaultFont", 12,), bg="#a7a7a7",highlightbackground="black")
        self.answer_entry.bind("<FocusIn>", lambda event: EventHandling.remove_highlight(event))
        self.answer_entry.place(x=100, y=130)

        self.confirm_answer = tk.Button(self, width=20, text="Confirm answer",command=self.check_answer)
        self.confirm_answer.config(bg="#a7a7a7", font=("TkDefaultFont", 12, "bold"), activebackground="#4f4f4f",relief="solid", borderwidth=3, cursor="hand2")
        self.confirm_answer.place(x=135, y=190)
        self.confirm_answer.bind("<Enter>", lambda event: EventHandling.button_hover(event, "#4f4f4f"))
        self.confirm_answer.bind("<Leave>", lambda event: EventHandling.button_leave(event, "#a7a7a7"))
        self.confirm_answer.bind("<Button-1>", lambda event: EventHandling.window_focus(self))

    def layout3(self):
        self.username_entry.place_forget()
        self.text_formula.place_forget()
        self.help_question.place_forget()
        self.answer_entry.place_forget()
        self.confirm_answer.place_forget()

        self.password_label = tk.Label(self, width=15, text="New password")
        self.password_label.config(background="#6c6c6c", fg="#282828", font=("TkDefaultFont", 12, "bold"), anchor=tk.W)
        self.password_label.place(x=95, y=25)

        self.new_password = tk.Entry(self, validate='key', validatecommand=self.vcmd, show="*")
        self.new_password.config(width=30, bd=5, font=("TkDefaultFont", 12,), bg="#a7a7a7")
        self.new_password.bind("<FocusIn>", lambda event: EventHandling.remove_highlight(event))
        self.new_password.place(x=100, y=50)

        ToolTip(self.new_password,msg="At least one major letter and a number must be included in the password. Passwords should be between three and nine characters long.")

        self.cfn_password_label = tk.Label(self, width=25, text="Confirm new password")
        self.cfn_password_label.config(background="#6c6c6c", fg="#282828", font=("TkDefaultFont", 12, "bold"))
        self.cfn_password_label.place(x=60, y=90)

        self.password_confirm = tk.Entry(self, validate='key', validatecommand=self.vcmd, show="*")
        self.password_confirm.config(width=30, bd=5, font=("TkDefaultFont", 12,), bg="#a7a7a7")
        self.password_confirm.bind("<FocusIn>", lambda event: EventHandling.remove_highlight(event))
        self.password_confirm.place(x=100, y=115)

        self.reset_password = tk.Button(self, width=20, text="Reset password", cursor="hand2", command=self.change_password)
        self.reset_password.config(bg="#a7a7a7", font=("TkDefaultFont", 12, "bold"), activebackground="#4f4f4f",relief="solid", borderwidth=3)
        self.reset_password.bind("<Enter>", lambda event: EventHandling.button_hover(event, "#4f4f4f"))
        self.reset_password.bind("<Leave>", lambda event: EventHandling.button_leave(event, "#a7a7a7"))
        self.reset_password.bind("<Button-1>", lambda event: EventHandling.window_focus(self))
        self.reset_password.place(x=135, y=160)

    def validate(self, value):
        if len(value) <= 9:
            return True
        else:
            return False

    def username_verification(self):
        username = self.username_entry.get()
        if username_exist(username):
            self.question = username_exist(username)
            self._init_layout2()
        else:
            self.username_entry.config(highlightthickness=2, highlightbackground='red')
            messagebox.showerror("Error", "Username doesn't exist")

    def check_answer(self):

        if answer_verification(self.username_entry.get(), self.answer_entry.get()):
            self.layout3()
        else:
            self.answer_entry.config(highlightthickness=2, highlightbackground='red')
            messagebox.showerror("Error", "Wrong answer")

    def change_password(self):

        password = self.new_password.get()
        regex = r"^(?=.*[A-Z])(?=.*\d)(?!.*[^\w]).{3,9}$"
        validation = True

        if not re.match(regex, password):
            validation = False
            self.new_password.config(highlightthickness=2, highlightbackground="red")
            messagebox.showerror("Error", "Password doesn't meet the requirements.")
        if self.password_confirm.get() != password:
            validation = False
            self.password_confirm.config(highlightthickness=2, highlightbackground="red")
            messagebox.showerror("Error", "Passwords aren't the same.")

        if validation:
            replace_password(self.username_entry.get(), password)
            messagebox.showinfo("Success", "Password changed")
            self.destroy()