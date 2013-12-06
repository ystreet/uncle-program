#!/usr/bin/python3

from gi.repository import Gtk

from filter import ProgramFilter
from program import Program, ProgramView, parse_program
from course import Course

data = [("awesome", "short desc"), ("awesomer", "shorter"), ("better", "shortest")]

def create_program ():
    p = Program("Dummy Program")
    for t, d in data:
        c = Course (t)
        c.short_desc = d
        p.courses.append (c)

    return p

class MainView:
    def __init__(self):
        self.window = Gtk.Window()
        self.window.set_border_width(10)

        self.screens = Gtk.Notebook()
        self.screens.set_show_tabs (False)
        self.screens.set_show_border (False)

        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)

#        p = create_program ()
        p = parse_program ("file:///home/matt/Projects/uncle-programs/test/test.htm")
#        print (p)
        self.screens.append_page (ProgramView (p), None)
        self.window.add (self.screens)

        self.window.show_all()

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        Gtk.main_quit()

    def main(self):
        Gtk.main()

if __name__ == "__main__":
    m = MainView()
    m.main()
