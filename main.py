#!/usr/bin/python3

from gi.repository import Gtk, GObject

from filter import ProgramFilter
from program import Program, ProgramView, parse_program
from course import Course, CourseView, parse_course

data = [("awesome", "short desc"), ("awesomer", "shorter"), ("better", "shortest")]

def create_program ():
    p = Program("Dummy Program")
    for t, d in data:
        c = Course (t)
        c.short_desc = d
        p.courses.append (c)

    return p

class MainView:
    current_course = None

    def __init__(self):
        self.window = Gtk.Window()
        self.window.set_border_width(10)

        self.screens = Gtk.Notebook()
        self.screens.set_show_tabs (False)
        self.screens.set_show_border (False)

        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)

        p = parse_program ("file:///home/matt/Projects/uncle-programs/test/test.htm")
        self.program = ProgramView (p)
        self.program.view_course.connect (self.view_course)
        self.screens.append_page (self.program, None)
        self.window.add (self.screens)

        self.window.show_all()

    def view_course (self, programview, course, data=None):
        value = GObject.Value(value_type=int)
        if self.current_course is not None:
            self.screens.remove_page (self.screens.page_num (self.current_course))

        self.current_course = CourseView (parse_course (course))
        self.current_course.show_all()
        self.screens.append_page (self.current_course, None)
        self.screens.child_get_property (self.current_course, "position", value)
        self.screens.set_current_page (value.get_value())
        self.screens.child_get_property (self.program, "position", value)
        self.screens.remove_page (value.get_value())

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        Gtk.main_quit()

    def main(self):
        Gtk.main()

if __name__ == "__main__":
    m = MainView()
    m.main()
