# Student Result Management System

A menu-driven Python application for managing student records and academic results,
built for the New Horizon Python Programming practical project.

## Features
- Add, view, search, update and delete students
- Record scores for at least 5 subjects, with total, average and grade
- Update scores, print individual report cards
- Sort results by average or name, show class statistics
- Save text reports to the `reports/` folder
- Data saved automatically to `data/students.json` and loaded on start-up
  (a missing or damaged file is handled safely)

## How to run
```bash
git clone https://github.com/adebanjotunmise13-web/student-result-system.git
cd student-result-system
python main.py
```

## Project structure
main.py      Entry point and menu
student.py   Student class, ID/date validation (regex), search and sorting
results.py   Scoring, grading and class statistics
storage.py   JSON load/save with error handling
reports.py   Report card, tables and saving reports to file
data/        students.json (created automatically)
reports/     Saved text reports

## Grading scale
Average Grade 
70-100 - A 
60-69 - B 
50-59 - C 
45-49 - D 
0-44 - F 

## Python concepts used
Variables and type conversion, if/elif/else, for and while loops, lists, tuples and
dictionaries, functions with return values, sorting (`sorted` with `key`),
try/except, file handling with JSON, multiple modules, a `Student` class (OOP with
properties, `from_dict` class method), `datetime` for dates, `re` for ID validation,
and the `os` module for paths and folders.
