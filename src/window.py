

from gi.repository import Adw, Gio, Gtk, GLib

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

        save_action = Gio.SimpleAction(name="save-as")
        save_action.connect("activate", self.save_file_dialog)
        self.add_action(save_action)

    def open_file_dialog(self, action, _):
        self._native = Gtk.FileChooserNative(
            title="Open File",
            transient_for=self,
            action=Gtk.FileChooserAction.OPEN,
            accept_label="_Open",
            cancel_label="_Cancel",
        )

        self._native.connect("response", self.on_open_response)
        self._native.show()

    def on_open_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            self.open_file(dialog.get_file())
        self._native = None

    def open_file(self, file):
        file.load_contents_async(None, self.open_file_complete)

    def open_file_complete(self, file, result):
        contents = file.load_contents_finish(result)
        if not contents[0]:
            path = file.peek_path()
            print(f"Unable to open {path}: {contents[1]}")

        try:
            text = contents[1].decode('utf-8')
        except UnicodeError as err:
            path = file.peek_path()
            print(f"Unable to open {path}: the file is not encoded properly")
            return

        buffer = self.main_text_view.get_buffer()
        buffer.set_text(text)
        start = buffer.get_start_iter()
        buffer.place_cursor(start)

    def save_file_dialog(self, action, _):
        self._native = Gtk.FileChooserNative(
            title="Save File As",
            transient_for=self,
            action=Gtk.FileChooserAction.SAVE,
            accept_label="_Save",
            cancel_label="_Cancel",
        )

        self._native.connect("response", self.on_save_response)
        self._native.show()

    def on_save_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            self.save_file(dialog.get_file())
        self._native = None

    def save_file(self, file):
        buffer = self.main_text_view.get_buffer()
        start = buffer.get_start_iter()
        end = buffer.get_end_iter()
        text = buffer.get_text(start, end, False)

        if not text:
            return

        byte = GLib.Bytes.new(text.encode('utf-8'))
        file.replace_contents_bytes_async(bytes, None, False, Gio.FileCreateFlags.NONE, None, self.save_file_complete)

    def save_file_complete(self, file, result):
        res = file.replace_contents_finish(result)
        info = file.query_info("standard::display-name", Gio.FileQueryInfoFlags.NONE)

        if info:
            display_name = info.get_attribute_string("standard::display-name")
        else:
            display_name = file.get_basename()

        if not res:
            print(f"Unable to save {display_name}")
