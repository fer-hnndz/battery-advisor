import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from ..utils import execute_action


class MessageAlert(Gtk.Dialog):
    TITLE = "Battery Advisor"

    def __init__(self, message):
        super().__init__(self.TITLE, transient_for=None)

        content = self.get_content_area()
        _title_label = Gtk.Label()
        _title_label.set_markup(f"<b>{self.TITLE}</b>")
        msg_label = Gtk.Label(message)

        content.add(_title_label)
        content.add(msg_label)

        if self.__class__ == MessageAlert:
            self.add_button("Close", Gtk.ResponseType.CLOSE)

        self.show_all()

    def run(self):
        response = super().run()
        if response == -4 or response == -7 or response == -1:
            response = 0

        return response


class AlertWithButtons(MessageAlert):
    def __init__(self, message, actions: list[str]):
        super().__init__(message)

        for i, action in enumerate(actions):
            self.add_button(action.capitalize(), i)

        self.show_all()
