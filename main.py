"""Student Result Management System - entry point and main menu."""
import reports
import results
import storage
import student as student_ops
from student import Student

SCHOOL_NAME = "New Horizon"
GENDERS = {"m": "Male", "f": "Female"}


#input_helpers
def ask(prompt):
    return input(prompt).strip()


def ask_required(prompt):
    while True:
        value = ask(prompt)
        if value:
            return value
        print("  This field cannot be empty.")


def ask_gender():
    while True:
        choice = ask("Gender (M/F): ").lower()
        if choice in GENDERS:
            return GENDERS[choice]
        print("  Please enter M or F.")


def ask_dob():
    while True:
        text = ask("Date of birth (YYYY-MM-DD): ")
        try:
            return student_ops.parse_date(text).strftime(student_ops.DATE_FORMAT)
        except ValueError as error:
            print(f"  Invalid date: {error} Use the format YYYY-MM-DD.")


def ask_score(subject):
    """Ask for a score; returns None if the user leaves it blank."""
    while True:
        text = ask(f"  {subject} (0-100, blank to skip): ")
        if text == "":
            return None
        try:
            return results.validate_score(text)
        except ValueError as error:
            print(f"  Invalid: {error}")


def pick_student(students):
    student_id = ask("Enter student ID: ")
    found = student_ops.find_by_id(students, student_id)
    if found is None:
        print("  Student not found.")
    return found


def pause():
    input("\nPress Enter to continue...")


#student_management
def add_student(students):
    print("\n--- Add New Student ---")
    while True:
        student_id = ask("Student ID (e.g. NH/2026/001): ")
        if not student_ops.is_valid_student_id(student_id):
            print("  Invalid ID. Use 3-15 letters, digits, '/', '-' or '_'.")
        elif student_ops.find_by_id(students, student_id):
            print("  That ID already exists.")
        else:
            break
    name = ask_required("Full name: ")
    class_name = ask_required("Class/Form: ")
    gender = ask_gender()
    dob = ask_dob()
    students.append(Student(student_id, name.title(), class_name, gender, dob))
    storage.save_students(students)
    print(f"  Student '{name.title()}' added.")


def view_students(students):
    print("\n--- Registered Students ---")
    if not students:
        print("  No students registered yet.")
        return
    for s in students:
        print(" ", s)
    print(f"\nTotal: {len(students)}")


def search_students(students):
    term = ask("\nSearch by ID or name: ")
    matches = student_ops.search(students, term)
    if not matches:
        print("  No matching student.")
    for s in matches:
        print(" ", s)


def update_student(students):
    print("\n--- Update Student ---")
    s = pick_student(students)
    if s is None:
        return
    print("Press Enter to keep the current value.")
    s.name = ask(f"Name [{s.name}]: ").title() or s.name
    s.class_name = ask(f"Class [{s.class_name}]: ") or s.class_name
    gender = ask(f"Gender M/F [{s.gender}]: ").lower()
    if gender in GENDERS:
        s.gender = GENDERS[gender]
    dob = ask(f"Date of birth [{s.dob}]: ")
    if dob:
        try:
            s.dob = student_ops.parse_date(dob).strftime(student_ops.DATE_FORMAT)
        except ValueError as error:
            print(f"  DOB not changed: {error}")
    storage.save_students(students)
    print("  Student updated.")


def delete_student(students):
    print("\n--- Delete Student ---")
    s = pick_student(students)
    if s is None:
        return
    if ask(f"Delete {s.name}? This cannot be undone (y/n): ").lower() == "y":
        students.remove(s)
        storage.save_students(students)
        print("  Student deleted.")
    else:
        print("  Cancelled.")


#scores
def record_scores(students):
    print("\n--- Record Scores ---")
    s = pick_student(students)
    if s is None:
        return
    print(f"Recording scores for {s.name}. At least {results.MIN_SUBJECTS} subjects are needed.")
    for subject in results.DEFAULT_SUBJECTS:
        score = ask_score(subject)
        if score is not None:
            s.set_score(subject, score)
    while ask("Add another subject? (y/n): ").lower() == "y":
        subject = ask_required("  Subject name: ").title()
        score = ask_score(subject)
        if score is not None:
            s.set_score(subject, score)
    if not s.has_complete_results:
        print(f"  Warning: only {len(s.scores)} subject(s) recorded; "
              f"{results.MIN_SUBJECTS} are required for a complete result.")
    storage.save_students(students)
    print("  Scores saved.")


def update_score(students):
    print("\n--- Update Score ---")
    s = pick_student(students)
    if s is None:
        return
    if not s.scores:
        print("  This student has no scores yet.")
        return
    for subject, score in s.scores.items():
        print(f"  {subject}: {score}")
    subject = ask("Subject to update: ").title()
    if subject not in s.scores:
        print("  That subject has not been recorded for this student.")
        return
    score = ask_score(subject)
    if score is None:
        print("  No change made.")
        return
    s.set_score(subject, score)
    storage.save_students(students)
    print("  Score updated.")


def show_report_card(students):
    s = pick_student(students)
    if s is None:
        return
    if not s.scores:
        print("  No scores recorded for this student yet.")
        return
    card = reports.report_card(s)
    print("\n" + card)
    if ask("\nSave this report card to a file? (y/n): ").lower() == "y":
        path = reports.save_report(card, f"report_card_{s.student_id.replace('/', '-')}.txt")
        if path:
            print(f"  Saved to {path}")


#reporting 
def list_results(students):
    scored = [s for s in students if s.scores]
    if not scored:
        print("\n  No results recorded yet.")
        return
    print("\nSort by: 1) Average (highest first)  2) Name")
    choice = ask("Choice: ")
    ordered = student_ops.sort_by_name(scored) if choice == "2" else student_ops.sort_by_average(scored)
    print("\n" + reports.results_table(ordered))


def show_statistics(students):
    print("\n" + reports.statistics_text(students))


def save_full_report(students):
    if not any(s.scores for s in students):
        print("\n  Nothing to report yet.")
        return
    path = reports.save_report(reports.full_report([s for s in students if s.scores]))
    if path:
        print(f"\n  Report saved to {path}")


#main menu
MENU = """
  {school} STUDENT RESULT MANAGEMENT SYSTEM
 1. Add student              8. Display report card
 2. View all students        9. List all results (sorted)
 3. Search student          10. Class statistics
 4. Update student          11. Save full report to file
 5. Delete student           0. Exit
 6. Record scores
 7. Update a score
"""


def main():
    students = storage.load_students()
    actions = {
        "1": add_student, "2": view_students, "3": search_students,
        "4": update_student, "5": delete_student, "6": record_scores,
        "7": update_score, "8": show_report_card, "9": list_results,
        "10": show_statistics, "11": save_full_report,
    }
    while True:
        print(MENU.format(school=SCHOOL_NAME.upper()))
        choice = ask("Enter choice: ")
        if choice == "0":
            storage.save_students(students)
            print("Data saved. Goodbye!")
            break
        action = actions.get(choice)
        if action is None:
            print("  Invalid choice, try again.")
            continue
        try:
            action(students)
        except (KeyboardInterrupt, EOFError):
            print("\n  Action cancelled.")
        except Exception as error:  # last-resort safety net
            print(f"  Unexpected error: {error}")
        pause()


if __name__ == "__main__":
    main()
