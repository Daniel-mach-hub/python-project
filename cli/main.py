import json
from data.storage import load_data, save_data

def show_menu():
    print("\n--- School Management CLI ---")
    print("1. Register a student")
    print("2. Add a course")
    print("3. Assign grade to student")
    print("4. View student grades")
    print("5. Exit")

def register_student(data):
    student = {
        "id": len(data["students"]) + 1,
        "name": input("Student Name: "),
        "email": input("Email: ")
    }
    data["students"].append(student)
    print("Student registered.")

def add_course(data):
    course = {
        "id": len(data["courses"]) + 1,
        "name": input("Course Name: ")
    }
    data["courses"].append(course)
    print("Course added.")

def show_courses(data):
    print("\nAvailable Courses:")
    for course in data["courses"]:
        print(f"{course['id']}: {course['name']}")

def assign_grade(data):
    try:
        student_id = int(input("Student ID: "))
    except ValueError:
        print("Invalid Student ID.")
        return

    student = next((s for s in data["students"] if s["id"] == student_id), None)
    if not student:
        print("Student not found.")
        return

    show_courses(data)

    try:
        course_id = int(input("Course ID: "))
        grade = input("Grade (e.g. A, B+): ")
    except ValueError:
        print("Invalid input.")
        return

    course = next((c for c in data["courses"] if c["id"] == course_id), None)
    if not course:
        print("Course not found.")
        return

    existing = next((g for g in data["grades"] if g["student_id"] == student_id and g["course_id"] == course_id), None)
    if existing:
        existing["grade"] = grade
    else:
        data["grades"].append({
            "student_id": student_id,
            "course_id": course_id,
            "grade": grade
        })

    print("Grade assigned.")

def view_grades(data):
    try:
        student_id = int(input("Enter student ID: "))
    except ValueError:
        print("Invalid Student ID.")
        return

    student = next((s for s in data["students"] if s["id"] == student_id), None)
    if not student:
        print("Student not found.")
        return

    print(f"\nGrades for {student['name']}:")
    student_grades = [g for g in data["grades"] if g["student_id"] == student_id]

    if not student_grades:
        print("No grades assigned.")
        return

    for record in student_grades:
        course = next(c for c in data["courses"] if c["id"] == record["course_id"])
        print(f"{course['name']}: {record['grade']}")

def main():
    data = load_data()

    # Only keep predefined courses; students and grades will be fresh
    if not data.get("courses"):
        data["courses"] = [
            {"id": 1, "name": "Mathematics"},
            {"id": 2, "name": "English"},
            {"id": 3, "name": "Computer Science"}
        ]

    if not data.get("students"):
        data["students"] = []

    if not data.get("grades"):
        data["grades"] = []

    while True:
        show_menu()
        choice = input("Choose an option: ")
        if choice == "1":
            register_student(data)
        elif choice == "2":
            add_course(data)
        elif choice == "3":
            assign_grade(data)
        elif choice == "4":
            view_grades(data)
        elif choice == "5":
            save_data(data)
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
