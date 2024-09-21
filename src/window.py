

from gi.repository import Adw, Gio, Gtk

@Gtk.Template(resource_path='/com/example/TextEditor/window.ui')
class TextEditorGtkWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'TextEditorGtkWindow'

    main_text_view = Gtk.Template.Child()
    open_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        open_action = Gio.SimpleAction(name="open")
        open_action.connect("activate", self.open_file_dialog)
        self.add_action(open_action)

    def open_file_dialog(self, action, _):
        pass
