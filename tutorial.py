import math
import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gdk, GLib, Gio  # noqa

css_provider = Gtk.CssProvider()
css_provider.load_from_path("style.css")
Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(
), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


class MainWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_default_size(600, 250)
        self.set_title("MyApp")

        self.box1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.box2.set_spacing(10)
        self.box2.set_margin_top(10)
        self.box2.set_margin_bottom(10)
        self.box2.set_margin_start(10)
        self.box2.set_margin_end(10)

        self.button = Gtk.Button(label="Hello")
        self.button.connect('clicked', self.hello)

        self.set_child(self.box1)
        self.box1.append(self.box2)
        self.box1.append(self.box3)

        self.box2.append(self.button)

        self.check = Gtk.CheckButton(label="And goodbye?")
        self.box2.append(self.check)

        self.radio1 = Gtk.CheckButton(label="test")
        self.radio2 = Gtk.CheckButton(label="test")
        self.radio3 = Gtk.CheckButton(label="test")
        self.radio2.set_group(self.radio1)
        self.radio3.set_group(self.radio1)

        self.box2.append(self.radio1)
        self.box2.append(self.radio2)
        self.box2.append(self.radio3)

        self.switch_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.switch = Gtk.Switch()
        self.switch.set_active(True)
        self.switch.connect("state-set", self.switch_switched)

        self.switch_box.append(self.switch)
        self.box2.append(self.switch_box)

        self.label = Gtk.Label(label="A switch")
        self.label.set_css_classes(['title'])
        self.switch_box.append(self.label)
        self.switch_box.set_spacing(5)

        self.slider = Gtk.Scale()
        self.slider.set_digits(0)  # number of decimal places to use
        self.slider.set_range(0, 10)
        self.slider.set_draw_value(True)  # show a label with current value
        self.slider.set_value(5)  # sets the current value/position
        self.slider.connect('value-changed', self.slider_changed)
        self.box2.append(self.slider)

        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)

        self.open_button = Gtk.Button(label="Open")
        self.open_button.set_icon_name("document-open-symbolic")
        self.open_button.connect('clicked', self.show_open_dialog)
        self.header.pack_start(self.open_button)

        self.open_dialog = Gtk.FileDialog.new()
        self.open_dialog.set_title("Select a File")

        f = Gtk.FileFilter()
        f.set_name("Image files")
        f.add_mime_type("image/png")
        f.add_mime_type("image/jpeg")

        # create a ListStore with the type Gtk.FileFilter
        filters = Gio.ListStore.new(Gtk.FileFilter)
        # add the file filter to the ListStore. You could add more.
        filters.append(f)

        # set the filters for the open dialog
        self.open_dialog.set_filters(filters)
        self.open_dialog.set_default_filter(f)

        # Menus
        # create a new action
        action = Gio.SimpleAction.new("something", None)
        action.connect("activate", self.print_something)
        # the action is being added to the window,
        # application or an "ActionGroup"
        self.add_action(action)

        # Create a new menu, containing that action
        menu = Gio.Menu.new()
        menu.append("Do Something", "win.something")

        # create a popover
        self.popover = Gtk.PopoverMenu()
        self.popover.set_menu_model(menu)

        # create a menu button
        self.hamburger = Gtk.MenuButton()
        self.hamburger.set_popover(self.popover)
        self.hamburger.set_icon_name("open-menu-symbolic")

        # add menu button to the header bar
        self.header.pack_end(self.hamburger)

        # set app name
        GLib.set_application_name("MyApp")

        # create action to run a *show about dialog* function
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.show_about)
        self.add_action(action)

        menu.append("About", "win.about")

        # drawing with cairo
        self.dw = Gtk.DrawingArea()

        # fill the available space
        self.dw.set_hexpand(True)
        self.dw.set_vexpand(True)

        self.dw.set_draw_func(self.draw, None)
        self.box3.append(self.dw)

        evk = Gtk.GestureClick.new()
        evk.connect("pressed", self.dw_click)
        self.dw.add_controller(evk)

        self.blobs = []

    def dw_click(self, gesture, data, x, y):
        self.blobs.append((x, y))
        self.dw.queue_draw()

    def show_open_dialog(self, button):
        self.open_dialog.open(self, None, self.open_dialog_open_callback)

    def open_dialog_open_callback(self, dialog, result):
        try:
            file = dialog.open_finish(result)
            if file is not None:
                print(f"File path is {file.get_path()}")
        except GLib.Error as error:
            print(f"Action failed: {error.message.lower()}")

    def slider_changed(self, slider):
        print(int(slider.get_value()))

    def switch_switched(self, switch, state):
        print(f"The switch has been switched {"on" if state else "off"}")

    def hello(self, button):
        print("Hello world")
        if self.check.get_active():
            print("Goodbye world!")
            self.close()

    def print_something(self, action, param):
        print("Something!")

    def show_about(self, action, param):
        # self.about = Gtk.AboutDialog()
        # # makes the dialog appear in front of the parent window
        # self.about.set_transient_for(self)
        # # makes the parent window unresponsive while dialog is showing
        # self.about.set_modal(True)
        #
        # self.about.set_authors(["It's me!"])
        # self.about.set_copyright("Copyright 2024 Me")
        # self.about.set_license_type(Gtk.License.GPL_3_0)
        # self.about.set_website("https://azr4e1.xyz")
        # self.about.set_website_label("My website")
        # self.about.set_version("1.0")
        # # self.about.set_logo_icon_name("org.example.example")
        #
        # self.about.set_visible(True)
        dialog = Adw.AboutWindow(transient_for=app.get_active_window())
        dialog.set_application_name("App name")
        dialog.set_version("1.0")
        dialog.set_developer_name("Developer")
        dialog.set_license_type(Gtk.License(Gtk.License.GPL_3_0))
        dialog.set_comments("Adw about Window example")
        dialog.set_website("https://github.com/Tailko2k/GTK4PythonTutorial")
        dialog.set_issue_url(
            "https://github.com/Tailko2k/GTK4PythonTutorial/issues")
        dialog.add_credit_section("Contributors", ["Name1 url"])
        dialog.set_translator_credits("Name1 url")
        dialog.set_copyright("© 2022 developer")
        dialog.set_developers(["Developer"])
        # icon must be uploaded in ~/.local/share/icons or /usr/share/icons
        dialog.set_application_icon("com.github.devname.appname")

        dialog.set_visible(True)

    def draw(self, area, c, w, h, data):
        # c is a cairo context
        # fill background with a color
        c.set_source_rgb(0, 0, 0)
        c.paint()

        c.set_source_rgb(1, 0, 1)
        for x, y in self.blobs:
            c.arc(x, y, 10, 0, 2 * math.pi)
            c.fill()

        # Draw a line
        c.set_source_rgb(0.5, 0.0, 0.5)
        c.set_line_width(3)
        c.move_to(10, 10)
        c.line_to(w-10, h-10)
        c.stroke()

        # Draw a rectangle
        c.set_source_rgb(0.8, 0.8, 0.0)
        c.rectangle(20, 20, 50, 20)
        c.fill()

        # Draw some text
        c.set_source_rgb(0.1, 0.1, 0.1)
        c.select_font_face("Sans")
        c.set_font_size(13)
        c.move_to(25, 35)
        c.show_text("test")


class MyApp(Adw.Application):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)
        self.connect('open', self.on_open)
        # need to tell GApplication we can handle this
        self.set_flags(Gio.ApplicationFlags.HANDLES_OPEN)
        self.win = None

    def on_activate(self, app):
        # check if application has been launched already
        if not self.win:
            self.win = MainWindow(application=app)
        self.win.present()

    def on_open(self, app, files, n_files, hint):
        # adding this because window may have not been created with this entry point
        self.on_activate(app)
        for file in files:
            print("File to open: " + file.get_path())


app = MyApp(application_id="com.example.GtkApplication")
app.run(sys.argv)
