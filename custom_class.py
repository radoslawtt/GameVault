class EventHandling:

    password_sentences = ["New password", "Confirm new password", "Password..."]
    different_sentences = ["New username", "New answer", "Username..."]

    @staticmethod
    def remove_highlight(event):
        event.widget.config(highlightthickness=0)

    @staticmethod
    def button_hover(event, background_color: str):
        event.widget.config(background=background_color)

    @staticmethod
    def button_leave(event, background_color: str):
        event.widget.config(background=background_color)

    @staticmethod
    def on_enter(event):

        if event.widget.get() in EventHandling.password_sentences:
            event.widget.delete(0, "end")
            event.widget.config(show="*")

        if event.widget.get() in EventHandling.different_sentences:
            event.widget.delete(0, "end")


    @staticmethod
    def on_leave(event, widget_id: str):

        #Widget_id = ExampleClassName_example_widget_name

        #ECN_example_widget_name
        #ChangePasswordWindow = CPW

        user_input = event.widget.get()

        if user_input == "":

            if widget_id == "CPW_new_password":
                event.widget.insert(0, "New password")
                event.widget.config(show="")

            if widget_id == "CPW_cfm_new_password":
                event.widget.insert(0, "Confirm new password")
                event.widget.config(show="")

            if widget_id == "LW_password_entry":
                event.widget.insert(0, "Password...")
                event.widget.config(show="")

            if widget_id == "CUW_new_username":
                event.widget.insert(0, "New username")

            if widget_id == "CSW_new_answer":
                event.widget.insert(0, "New answer")

            if widget_id == "LW_username_entry":
                event.widget.insert(0, "Username...")

    @staticmethod
    def window_focus(window):
        window.focus_set()