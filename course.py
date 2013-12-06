from gi.repository import Gtk

class CourseType:
    NONE = 0
    REQUIRED = 1
    DIRECTED = 2

class Course:
    name = ""
    short_desc = ""
    description = ""
    link = ""
    type = CourseType.NONE

    def __init__ (self, name, type=CourseType.NONE):
        self.name = name
        self.type = type

    def __eq__ (self, other):
        if type(other) is not Course: return False
        if self.name != other.name: return False
        if self.type != other.type: return False
        if self.short_desc != other.short_desc: return False
        if self.description != other.description: return False
        if self.link != other.link: return False
        return True

    def __str__ (self):
        return "<Course %s, %i, %s>" % (self.name, self.type, self.link)

class CourseView (Gtk.Box):
    course = None
    name = None
    short_desc = None
    sep = None

    def __init__ (self, course):
        Gtk.HBox.__init__ (self, orientation=Gtk.Orientation.HORIZONTAL)
        self.name = Gtk.Label ("")
        self.sep = Gtk.Label (" --- ")
        self.short_desc = Gtk.Label ("")
        self.pack_start (self.name, False, True, 0)
        self.pack_start (self.sep, False, True, 0)
        self.pack_start (self.short_desc, False, True, 0)

        self._set_course (course)

    def _set_course (self, course):
        self.name.set_text (course.name)
        self.short_desc.set_text (course.short_desc)

