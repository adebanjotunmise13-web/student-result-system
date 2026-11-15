"""Score calculation and grading logic."""

MIN_SUBJECTS = 5
DEFAULT_SUBJECTS = (
    "English", "Mathematics", "Physics", "Chemistry", "Biology", "Civic Education",
)

GRADE_BOUNDARIES = ((70, "A"), (60, "B"), (50, "C"), (45, "D"))


def grade_from_average(average):
    """Return a letter grade for an average score."""
    for minimum, letter in GRADE_BOUNDARIES:
        if average >= minimum:
            return letter
    return "F"


def remark_for_grade(grade):
    remarks = {"A": "Excellent", "B": "Very Good", "C": "Good",
               "D": "Pass", "F": "Fail"}
    return remarks.get(grade, "")


def calculate_total(scores):
    return sum(scores.values())


def calculate_average(scores):
    """Average of all scores; 0.0 if there are no scores."""
    if not scores:
        return 0.0
    return calculate_total(scores) / len(scores)


def validate_score(value):
    """Convert text to a float between 0 and 100, or raise ValueError."""
    score = float(value)  
    if not 0 <= score <= 100:
        raise ValueError("Score must be between 0 and 100.")
    return score


def class_statistics(students):
    """Return a dict of class statistics, or None if no student has scores."""
    scored = [s for s in students if len(s.scores) > 0]
    if not scored:
        return None

    all_scores = [(score, subject, s.name)
                  for s in scored for subject, score in s.scores.items()]
    highest = max(all_scores)
    lowest = min(all_scores)
    averages = [s.average for s in scored]
    best = max(scored, key=lambda s: s.average)
    worst = min(scored, key=lambda s: s.average)

    return {
        "students": len(scored),
        "highest_score": highest,  
        "lowest_score": lowest,
        "class_average": sum(averages) / len(averages),
        "top_student": best,
        "bottom_student": worst,
    }
