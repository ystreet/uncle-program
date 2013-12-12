from gi.repository import Gtk, GObject

from lxml import etree
import re

from requirement import CourseDependency

courses = []

def is_course_code (code):
    return type(code) == str \
            and len(code) == 8 \
            and code[:4].isalpha () \
            and code[4:].isdigit()

class CourseType:
    NONE = "NONE"
    REQUIRED = "REQUIRED"
    DIRECTED = "DIRECTED"

def get_course (code):
    for c in courses:
        if c.code == code:
            return c
    return Course (code)

def parse_course (course):
    if not course.link:
        return course

    parser = etree.HTMLParser(remove_blank_text=True)
    tree = etree.parse (course.link, parser)
    content = '/descendant::div[attribute::class="content-main"]/div[attribute::class="feed-page"]'
    place = tree.xpath (content)[0]
    result = etree.tostring (place, pretty_print=True, method="html")

    for elem in place:
        if elem.tag == "h1" and elem.get ("class") == "course-title":
            course.name = elem.text
        elif elem.tag == "table" and elem.get ("class") == "course-meta-details":
            info_path = tree.getpath(elem) + "/tr/td"
            info = tree.xpath (info_path)
            for i in info:
                s = "".join ((j for j in i.itertext()))
                course = parse_course_info (course, s)

            course_overview_path = content + '/descendant::p[attribute::class="course-overview"]'
            course_overview = tree.xpath (course_overview_path)
            course.description = "\n\n".join((i for i in course_overview[0].itertext()))
            course_details_path = content + '/descendant::table[attribute::class="course-details-table"]'
            course_details = tree.xpath (course_details_path)
            for table in course_details:
                course_availability_path = tree.getpath(table) + '/descendant::table[attribute::class="course-availability-table"]'
                course_availability = tree.xpath (course_availability_path)
                if len (course_availability) > 0:
                    pass
                else:
                    headers_path = tree.getpath (table) + '/descendant::th'
                    data_path = tree.getpath (table) + '/descendant::td'
                    headers = [i for i in (("\n".join(j.itertext()) for j in tree.xpath (headers_path)))]
                    data = [i for i in (("\n".join (j.itertext()) for j in tree.xpath (data_path)))]

                    for i in range(min(len(headers), len(data))):
                        course = parse_data (course, headers[i], data[i])
    return course

def parse_course_info (course, string):
    if string.startswith ("Course Code"):
        course.code = string.replace ("Course Code", "").strip()
    elif string.startswith("Units"):
        course.n_units = int(string.replace ("Units", "").strip())
    elif string.startswith ("Level"):
        course.level = int (string.replace ("Level", "").strip())
    return course

def find_course_code_iter (data, course):
    words = re.findall(r"[\w']+", data)
    for w in words:
        if is_course_code (w) and w != course.code and w not in [i.code for i in course.requirements if type (i) == CourseDependency]:
            yield w

def parse_data (course, head, data):
    head = head.lower()
    print (head, "***", data)
    if "objectives" in head:
        course.objectives = data
    elif "content" in head:
        course.content = data
    elif "replacing" in head:
        for code in find_course_code_iter (data, course):
            pass
    elif "transition" in head:
        for code in find_course_code_iter (data, course):
            pass
    elif "industrial experience" in head:
        pass
    elif "assumed knowledge" in head:
        for code in find_course_code_iter (data, course):
            req = CourseDependency (code)
            course.requirements.append (req)
    elif "delivery" in head:
        data = data.lower()
        if "internal" in data:
            course.modes.append("Internal")
        if "external" in data:
            course.modes.append("External")
        if not course.modes:
            course.modes = ["Unknown"]
    elif "teaching methods" in head:
        pass
    elif "compulsory course component" in head:
        pass
    elif "assessment items" in head:
        course.assessment_items = data.split ("\n")
    return course

class Course:
    code = ""
    name = ""
    n_units = 0
    level = 0
    description = ""
    link = ""
    comment = ""
    requirements = []
    school = ""
    modes = []
    assessment_items = []

    def __init__ (self, code):
        self.code = code

    def __eq__ (self, other):
        if type(other) is not Course: return False
        if self.code != other.code: return False
        return True

    def __str__ (self):
        return "<Course %s, %s, %s>" % (self.code, self.type, self.link)

class CourseView (Gtk.Grid):
    course = None

    def __init__ (self, course):
        Gtk.Grid.__init__ (self)

        self.set_row_spacing (5)
        self.set_column_spacing (5)
        self.set_border_width (3)

        self.title = Gtk.Label ("")
        self.title.set_hexpand (expand=True)
        self.attach (self.title, 0, 0, 2, 1)

        # Level
        self.units_lbl = Gtk.Label("No Units:")
        self.units_lbl.set_halign (align=Gtk.Align.START)
        self.units_lbl.set_valign (align=Gtk.Align.START)
        self.units = Gtk.Label("")
        self.units.set_halign (align=Gtk.Align.START)
        self.units.set_hexpand (expand=True)
        self.attach (self.units_lbl, 0, 1, 1, 1)
        self.attach (self.units, 1, 1, 1, 1)

        # Level
        self.level_lbl = Gtk.Label("Level:")
        self.level_lbl.set_halign (align=Gtk.Align.START)
        self.level_lbl.set_valign (align=Gtk.Align.START)
        self.level = Gtk.Label("")
        self.level.set_halign (align=Gtk.Align.START)
        self.level.set_hexpand (expand=True)
        self.attach (self.level_lbl, 0, 2, 1, 1)
        self.attach (self.level, 1, 2, 1, 1)

        # delivery mode
        self.mode_lbl = Gtk.Label("Delivery Modes:")
        self.mode_lbl.set_halign (align=Gtk.Align.START)
        self.mode_lbl.set_valign (align=Gtk.Align.START)
        self.mode = Gtk.Label("")
        self.mode.set_halign (align=Gtk.Align.START)
        self.mode.set_hexpand (expand=True)
        self.attach (self.mode_lbl, 0, 3, 1, 1)
        self.attach (self.mode, 1, 3, 1, 1)

        # delivery mode
        self.school_lbl = Gtk.Label("School:")
        self.school_lbl.set_halign (align=Gtk.Align.START)
        self.school_lbl.set_valign (align=Gtk.Align.START)
        self.school = Gtk.Label("")
        self.school.set_halign (align=Gtk.Align.START)
        self.school.set_hexpand (expand=True)
        self.attach (self.school_lbl, 0, 4, 1, 1)
        self.attach (self.school, 1, 4, 1, 1)

        # assessment items
        self.assessment_lbl = Gtk.Label("Assessment Items:")
        self.assessment_lbl.set_halign (align=Gtk.Align.START)
        self.assessment_lbl.set_valign (align=Gtk.Align.START)
        self.assessment = Gtk.Label("")
        self.assessment.set_halign (align=Gtk.Align.START)
        self.assessment.set_line_wrap (True)
        self.assessment.set_justify (Gtk.Justification.LEFT)
        self.attach (self.assessment_lbl, 0, 5, 1, 1)
        self.attach (self.assessment, 1, 5, 1, 1)

        # description
        self.desc_box = Gtk.Expander(label="Description")
        self.desc_box.set_halign (align=Gtk.Align.START)
        self.desc = Gtk.Label("")
        self.desc.set_line_wrap (True)
        self.desc.set_halign (align=Gtk.Align.FILL)
        self.desc_box.add (self.desc)
        self.attach (self.desc_box, 0, 10, 2, 1)

        # objectives
        self.obj_box = Gtk.Expander(label="Objectives")
        self.obj_box.set_halign (align=Gtk.Align.START)
        self.obj = Gtk.Label("")
        self.obj.set_line_wrap (True)
        self.obj.set_halign (align=Gtk.Align.FILL)
        self.obj_box.add (self.obj)
        self.attach (self.obj_box, 0, 11, 2, 1)

        # content
        self.content_box = Gtk.Expander(label="Content")
        self.content_box.set_halign (align=Gtk.Align.START)
        self.content = Gtk.Label("")
        self.content.set_line_wrap (True)
        self.content.set_halign (align=Gtk.Align.FILL)
        self.content_box.add (self.content)
        self.attach (self.content_box, 0, 12, 2, 1)

        self._set_course (course)

    def _set_course (self, course):
        self.course = course
        self.title.set_text (course.code + " - " + course.name)
        self.mode.set_text ("\n".join ((i for i in course.modes)))
        self.level.set_text (str(course.level))
        self.units.set_text (str(course.n_units))
        self.desc.set_text (course.description)
        self.obj.set_text (course.objectives)
        self.content.set_text (course.content)
        self.assessment.set_text ("\n".join ((i for i in course.assessment_items)))

