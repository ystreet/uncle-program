from gi.repository import Gtk, GObject

from course import Course

class Major:
    name = ""
    description = ""
    requirements = []
    courses = []

    def __init__(self, name):
        self.name = name

class MajorCourseView (Gtk.Box):
    course = None
    code = None
    name = None
    sep = None

    def __init__ (self, course):
        Gtk.HBox.__init__ (self, orientation=Gtk.Orientation.HORIZONTAL)
        self.code = Gtk.Button ("")
        self.code.connect ("clicked", self.on_click)
        self.sep = Gtk.Label (" --- ")
        self.name = Gtk.Label ("")
        self.pack_start (self.code, False, True, 0)
        self.pack_start (self.sep, False, True, 0)
        self.pack_start (self.name, False, True, 0)

        self._set_course (course)

    def _set_course (self, course):
        self.course = course
        self.code.set_label (course.code)
        self.name.set_text (course.name)

    @GObject.Signal
    def clicked (self):
        pass

    def on_click (self, widget, data=None):
        self.clicked.emit ()

class MajorView (Gtk.Expander):
    major = None
    box = None
    view_course = None

    def __init__ (self, major):
        Gtk.Expander.__init__ (self, label=major.name)
        self.box = Gtk.Box (orientation=Gtk.Orientation.VERTICAL)
        self.add (self.box)

        self._set_major (major)

    def _set_major (self, major):
        for c in major.courses:
            cv = MajorCourseView (c)
            cv.clicked.connect (self.on_course_clicked)
            self.box.pack_start (cv, False, True, 0)
        self.major = major

    def on_course_clicked (self, widget, data=None):
        self.view_course.emit (widget.course)

    @GObject.Signal(flags=GObject.SignalFlags.RUN_LAST)
    def view_course (self, course:GObject.TYPE_PYOBJECT):
        pass
