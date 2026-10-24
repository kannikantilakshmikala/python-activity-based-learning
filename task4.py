# Examination Result and Grace-Mark Validation

PASS_MARK = 35
MAX_MARKS = 100
MAX_TOTAL_GRACE = 5
MAX_GRACE_PER_SUBJECT = 3


def classify_result(percentage):
    if percentage >= 75:
        return "Distinction"
    elif percentage >= 60:
        return "First Class"
    elif percentage >= 50:
        return "Second Class"
    elif percentage >= 35:
        return "Pass"
    else:
        return "Fail"


def process_results(subjects):
    # Identify subjects where the student has failed
    failed_subjects = [
        subject for subject in subjects
        if subject["marks"] < PASS_MARK
    ]

    grace_used = 0

    # Apply grace marks only if the student can pass within
    # the configured per-subject and total grace limits.
    for subject in failed_subjects:
        required = PASS_MARK - subject["marks"]

        if (
            required <= MAX_GRACE_PER_SUBJECT
            and grace_used + required <= MAX_TOTAL_GRACE
        ):
            subject["grace"] = required
            subject["final_marks"] = min(
                subject["marks"] + required, MAX_MARKS
            )
            grace_used += required
        else:
            subject["grace"] = 0
            subject["final_marks"] = subject["marks"]

    # Subjects that already passed do not need grace marks
    for subject in subjects:
        if "final_marks" not in subject:
            subject["grace"] = 0
            subject["final_marks"] = min(
                subject["marks"], MAX_MARKS
            )

    # Check final pass status for every subject
    all_passed = all(
        subject["final_marks"] >= PASS_MARK
        for subject in subjects
    )

    total_marks = sum(
        subject["final_marks"] for subject in subjects
    )
    maximum_total = len(subjects) * MAX_MARKS
    percentage = (total_marks / maximum_total) * 100

    if all_passed:
        classification = classify_result(percentage)
        result = "PASS"
    else:
        classification = "Fail"
        result = "FAIL"

    return total_marks, percentage, grace_used, result, classification


def main():
    print("=" * 65)
    print("       EXAMINATION RESULT AND GRACE-MARK VALIDATION")
    print("=" * 65)

    try:
        student_id = input("Enter student ID: ").strip()
        student_name = input("Enter student name: ").strip()

        if not student_id or not student_name:
            print("Student ID and name cannot be empty.")
            return

        number_of_subjects = int(input("Enter number of subjects: "))

        if number_of_subjects <= 0:
            print("Number of subjects must be greater than zero.")
            return

        subjects = []

        for i in range(number_of_subjects):
            print(f"\nSubject {i + 1}")
            name = input("Enter subject name: ").strip()

            if not name:
                print("Subject name cannot be empty.")
                return

            marks = float(input("Enter marks (0-100): "))

            if marks < 0 or marks > MAX_MARKS:
                print("Marks must be between 0 and 100.")
                return

            subjects.append({
                "name": name,
                "marks": marks
            })

    except ValueError:
        print("Invalid input. Enter valid numbers for subjects and marks.")
        return

    total, percentage, grace, result, classification = (
        process_results(subjects)
    )

    # Display final mark sheet
    print("\n" + "=" * 75)
    print("                       FINAL MARK SHEET")
    print("=" * 75)
    print(f"Student ID   : {student_id}")
    print(f"Student Name : {student_name}")
    print("-" * 75)

    print(
        f"{'Subject':<20}{'Original Marks':>18}"
        f"{'Grace Marks':>15}{'Final Marks':>15}"
    )
    print("-" * 75)

    for subject in subjects:
        print(
            f"{subject['name']:<20}"
            f"{subject['marks']:>18.1f}"
            f"{subject['grace']:>15.1f}"
            f"{subject['final_marks']:>15.1f}"
        )

    print("-" * 75)
    print(f"Total Marks      : {total:.1f} / {number_of_subjects * MAX_MARKS}")
    print(f"Percentage       : {percentage:.2f}%")
    print(f"Grace Marks Used : {grace}")
    print(f"Final Result     : {result}")
    print(f"Classification   : {classification}")
    print("=" * 75)


if __name__ == "__main__":
    main()
