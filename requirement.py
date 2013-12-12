class Requirement:
    description = ""

    def check (self, program):
        """
        Returns: (success, reason)
        """
        raise NotImplementedError


class Conflict (Requirement):
    pass

class CourseConflict (Conflict):
    def __init__ (self, code):
        self.code = code

    def check (self, program):
        for c in program.courses:
            if c.code == self.code:
                return False, ""
        return False, "Required dependency not satisfied. %s" % self.code

class Dependency (Requirement):
    pass

class CourseDependency (Dependency):
    def __init__(self, code):
        self.code = code

    def check (self, program):
        for c in program.courses:
            if c.code == self.code:
                return True, ""
        return False, "Required dependency not satisfied. %s" % self.code

    def __str__ (self):
        return "<CourseDependency on %s>" % self.code
