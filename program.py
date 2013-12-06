from gi.repository import Gtk
from course import Course, CourseView, CourseType
from major import Major, MajorView

from lxml import etree

class Program:
    name = ""
    short_desc = ""
    description = ""
    courses = []
    majors = []

    def __init__ (self, name):
        self.name = name

    def __str__ (self):
        return "<Program %s - %s>" % (self.name, self.short_desc)

def parse_program (site):
    program = Program ("")
    parser = etree.HTMLParser(remove_blank_text=True)
    tree = etree.parse (site, parser)
    content = '/descendant::div[attribute::class="content-main"]'
    place = tree.xpath (content)[0]

    result = etree.tostring (place, pretty_print=True, method="html")

    majors_path = content + "/descendant::table[contains(@class, 'majorTable')]"
    for m in tree.xpath (majors_path):
#        print (etree.tostring (m, pretty_print=True, method="html"))
        m_path = tree.getpath(m)
        title_path = m_path + "/thead/descendant::a[attribute::class='title']/text()"
        major_title = tree.xpath (title_path)[0]
#        print (major_title)
        
        maj = Major (major_title)
        course_path = m_path + "/descendant-or-self::table[contains(@class, 'courseTable')]"
        for course in tree.xpath (course_path):
#            print ()
            maj.courses = parse_course_table (program, tree, course)
        program.majors.append (maj)
    return program
#        break

def parse_course_table (p, tree, table):
    courses = []
#    print (table.get("id"))
    course_type_path = tree.getpath (table) + "/descendant::a[contains(@class, 'title')]/text()"
    course_type = tree.xpath(course_type_path)[0]
#    print (course_type)

    codes_path = tree.getpath (table) + "/descendant::td[contains(@class, 'code')]/a"
    codes = tree.xpath (codes_path)
#    print (codes)
#    print ([a.get ("href") for a in codes])
#    print ([a.text for a in codes])
    codes_title_path = tree.getpath (table) + "/descendant::td[contains(@class, 'title')]/a/text()"
    codes_title = tree.xpath (codes_title_path)
    if len(codes) != len(codes_title) or len(codes) != len(codes_title):
#        print ("Error: lengths don't match with codes and codes_title")
        return []

    for i in range (len (codes)):
        c = Course(codes[i].text)
        c.type = parse_course_type (course_type)
        c.short_desc = codes_title[i]
        c.link = codes[i].get ("href")
#        print (c)
        courses.append (c)
    return courses

def parse_course_type (t):
    t = t.lower()
    t = t.replace ("courses", "").strip()
    if t == "core": return CourseType.REQUIRED
    if t == "directed": return CourseType.DIRECTED
    if t == "compulsory": return CourseType.REQUIRED
    return CourseType.NONE

class ProgramView (Gtk.Box):
    program = None

    def __init__ (self, program):
        Gtk.Box.__init__ (self, orientation=Gtk.Orientation.VERTICAL)

        self.name = Gtk.Label("")
        self.pack_start (self.name, True, False, 0)

        self._set_program (program)

    def _set_program (self, program):
        self.program = program

        self.name.set_text (program.name)

        for m in program.majors:
            self.pack_start (MajorView (m), False, True, 0)
