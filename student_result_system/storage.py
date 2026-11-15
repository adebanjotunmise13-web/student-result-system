"""Load and save student data as JSON."""
import json
import os

from student import Student

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "students.json")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")


def load_students(path=DATA_FILE):
    """Return a list of Student objects. Missing or corrupt files give an empty list."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            raw = json.load(file)
        return [Student.from_dict(item) for item in raw]
    except FileNotFoundError:
        print("No data file found - starting with an empty system.")
        return []
    except (json.JSONDecodeError, KeyError, TypeError):
        print("Warning: data file is damaged. Starting empty (old file kept as .bak).")
        try:
            os.replace(path, path + ".bak")
        except OSError:
            pass
        return []


def save_students(students, path=DATA_FILE):
    """Write all students to disk. Returns True on success."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            json.dump([s.to_dict() for s in students], file, indent=4)
        return True
    except OSError as error:
        print(f"Error: could not save data ({error}).")
        return False
