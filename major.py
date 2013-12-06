from gi.repository import Gtk

from course import Course, CourseView

class Major:
    name = ""
    description = ""
    requirements = []
    courses = []

    def __init__(self, name):
        self.name = name

class MajorView (Gtk.Expander):
    major = None
    box = None

    def __init__ (self, major):
        Gtk.Expander.__init__ (self, label=major.name)
        self.box = Gtk.Box (orientation=Gtk.Orientation.VERTICAL)
        self.add (self.box)

        self._set_major (major)

    def _set_major (self, major):
        for c in major.courses:
            self.box.pack_start (CourseView (c), False, True, 0)
