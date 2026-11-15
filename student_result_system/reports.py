"""Report generation (text output and saving to file)."""
import os
from datetime import datetime

import results
import student as student_ops
from storage import REPORTS_DIR

LINE = "=" * 70


def report_card(s):
    lines = [LINE, "STUDENT REPORT CARD".center(70), LINE,
             f"ID     : {s.student_id}",
             f"Name   : {s.name}",
             f"Class  : {s.class_name}      Gender: {s.gender}      DOB: {s.dob}",
             "-" * 70,
             f"{'Subject':<30}{'Score':>10}{'Grade':>10}",
             "-" * 70]
    for subject, score in s.scores.items():
        lines.append(f"{subject:<30}{score:>10.1f}{results.grade_from_average(score):>10}")
    lines += ["-" * 70,
              f"Total   : {s.total:.1f}",
              f"Average : {s.average:.2f}",
              f"Grade   : {s.grade} ({results.remark_for_grade(s.grade)})",
              f"Results entered: {s.date_entered or 'N/A'}",
              LINE]
    return "\n".join(lines)


def results_table(students, title="ALL STUDENTS' RESULTS"):
    lines = [LINE, title.center(70), LINE,
             f"{'#':<4}{'ID':<14}{'Name':<24}{'Total':>9}{'Average':>10}{'Grade':>8}",
             "-" * 70]
    for position, s in enumerate(students, start=1):
        lines.append(f"{position:<4}{s.student_id:<14}{s.name[:22]:<24}"
                     f"{s.total:>9.1f}{s.average:>10.2f}{s.grade:>8}")
    lines.append(LINE)
    return "\n".join(lines)


def statistics_text(students):
    stats = results.class_statistics(students)
    if stats is None:
        return "No scores recorded yet, so there are no class statistics."
    score, subject, name = stats["highest_score"]
    low_score, low_subject, low_name = stats["lowest_score"]
    return "\n".join([
        LINE, "CLASS STATISTICS".center(70), LINE,
        f"Students with results : {stats['students']}",
        f"Class average         : {stats['class_average']:.2f}",
        f"Highest single score  : {score:.1f} ({subject}, {name})",
        f"Lowest single score   : {low_score:.1f} ({low_subject}, {low_name})",
        f"Best student          : {stats['top_student'].name} ({stats['top_student'].average:.2f})",
        f"Weakest student       : {stats['bottom_student'].name} ({stats['bottom_student'].average:.2f})",
        LINE])


def full_report(students):
    """Complete class report as one text block."""
    header = f"STUDENT RESULT REPORT - generated {datetime.now():%Y-%m-%d %H:%M}"
    parts = [header, "",
             results_table(student_ops.sort_by_average(students), "RANKING BY AVERAGE"),
             "", statistics_text(students)]
    return "\n".join(parts)


def save_report(text, filename=None):
    """Save text to the reports folder and return the file path (or None on error)."""
    if filename is None:
        filename = f"report_{datetime.now():%Y%m%d_%H%M%S}.txt"
    path = os.path.join(REPORTS_DIR, filename)
    try:
        os.makedirs(REPORTS_DIR, exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            file.write(text + "\n")
        return path
    except OSError as error:
        print(f"Error: could not save report ({error}).")
        return None
