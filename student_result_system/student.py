"""Student class and input-validation helpers."""
import re
from datetime import datetime

import results

ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9/_-]{2,14}$")
DATE_FORMAT = "%Y-%m-%d"


def is_valid_student_id(student_id):
    """IDs are 3-15 characters: letters, digits, '/', '-' or '_' (e.g. NH/2026/001)."""
    return bool(ID_PATTERN.match(student_id))


def parse_date(text):
    """Parse YYYY-MM-DD into a date; raises ValueError if invalid or in the future."""
    parsed = datetime.strptime(text.strip(), DATE_FORMAT).date()
    if parsed > datetime.now().date():
        raise ValueError("Date of birth cannot be in the future.")
    return parsed


class Student:
    """A student and their scores."""

    def __init__(self, student_id, name, class_name, gender, dob,
                 scores=None, date_entered=None):
        self.student_id = student_id
        self.name = name
        self.class_name = class_name
        self.gender = gender
        self.dob = dob                      # string YYYY-MM-DD
        self.scores = scores or {}          # {subject: score}
        self.date_entered = date_entered    # when results were last recorded

    #properties
    @property
    def total(self):
        return results.calculate_total(self.scores)

    @property
    def average(self):
        return results.calculate_average(self.scores)

    @property
    def grade(self):
        if not self.scores:
            return "-"
        return results.grade_from_average(self.average)

    @property
    def has_complete_results(self):
        return len(self.scores) >= results.MIN_SUBJECTS

    #score_handling
    def set_score(self, subject, score):
        self.scores[subject] = score
        self.date_entered = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #saving
    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "class_name": self.class_name,
            "gender": self.gender,
            "dob": self.dob,
            "scores": self.scores,
            "date_entered": self.date_entered,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["student_id"], data["name"], data["class_name"],
            data["gender"], data["dob"],
            data.get("scores", {}), data.get("date_entered"),
        )

    def __str__(self):
        return f"{self.student_id} | {self.name} | {self.class_name} | {self.gender} | {self.dob}"


#operations
def find_by_id(students, student_id):
    for student in students:
        if student.student_id.lower() == student_id.strip().lower():
            return student
    return None


def search(students, term):
    """Return students whose ID or name contains the search term."""
    term = term.strip().lower()
    return [s for s in students
            if term in s.student_id.lower() or term in s.name.lower()]


def sort_by_average(students):
    return sorted(students, key=lambda s: s.average, reverse=True)


def sort_by_name(students):
    return sorted(students, key=lambda s: s.name.lower())
