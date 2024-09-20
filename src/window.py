

from gi.repository import Adw
from gi.repository import Gtk

@Gtk.Template(resource_path='/com/example/TextEditor/window.ui')
class TextEditorGtkWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'TextEditorGtkWindow'

    main_text_view = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
