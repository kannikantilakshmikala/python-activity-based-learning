# University Scholarship Allocation System

MIN_AGGREGATE = 75
MIN_SUBJECT_MARK = 60
MIN_ATTENDANCE = 75
MAX_FAMILY_INCOME = 300000

def evaluate_applicant(applicant):
    marks = applicant["marks"]
    aggregate = sum(marks.values()) / len(marks)

    # Check eligibility criteria
    if aggregate < MIN_AGGREGATE:
        return False, aggregate, "Aggregate marks below 75%"

    if any(mark < MIN_SUBJECT_MARK for mark in marks.values()):
        return False, aggregate, "Subject score below 60"

    if applicant["attendance"] < MIN_ATTENDANCE:
        return False, aggregate, "Attendance below 75%"

    if applicant["income"] > MAX_FAMILY_INCOME:
        return False, aggregate, "Family income exceeds limit"

    return True, aggregate, "Eligible"


def main():
    applicants = []

    try:
        n = int(input("Enter number of applicants: "))
        if n <= 0:
            print("Number of applicants must be positive.")
            return
    except ValueError:
        print("Invalid number of applicants.")
        return

    for i in range(n):
        print(f"\n--- Applicant {i + 1} ---")

        student_id = input("Enter student ID: ").strip()
        name = input("Enter student name: ").strip()

        if not student_id or not name:
            print("ID and name cannot be empty.")
            return

        if any(a["id"] == student_id for a in applicants):
            print("Duplicate student ID. Please restart the program.")
            return

        # Collect marks
        subjects = {}
        try:
            subject_count = int(input("Enter number of subjects: "))
            if subject_count <= 0:
                print("Subject count must be positive.")
                return

            for j in range(subject_count):
                subject = input(f"Enter subject {j + 1} name: ").strip()

                if not subject or subject in subjects:
                    print("Subject name cannot be empty or duplicated.")
                    return

                mark = float(input(f"Enter marks for {subject} (0-100): "))

                if not 0 <= mark <= 100:
                    print("Marks must be between 0 and 100.")
                    return

                subjects[subject] = mark

            attendance = float(input("Enter attendance percentage: "))
            income = float(input("Enter annual family income (Rs.): "))

            if not 0 <= attendance <= 100 or income < 0:
                print("Invalid attendance or income.")
                return

        except ValueError:
            print("Invalid numeric input.")
            return

        applicants.append({
            "id": student_id,
            "name": name,
            "marks": subjects,
            "attendance": attendance,
            "income": income
        })

    # Evaluate eligibility
    eligible = []
    rejected = []

    for applicant in applicants:
        status, aggregate, reason = evaluate_applicant(applicant)

        applicant["aggregate"] = aggregate
        applicant["status"] = reason

        if status:
            eligible.append(applicant)
        else:
            rejected.append(applicant)

    # Ranking policy:
    # 1. Higher aggregate marks
    # 2. Higher attendance
    # 3. Lower family income
    eligible.sort(
        key=lambda a: (
            -a["aggregate"],
            -a["attendance"],
            a["income"],
            a["id"]
        )
    )

    # Display eligible ranking
    print("\n" + "=" * 85)
    print("          UNIVERSITY SCHOLARSHIP RANKING")
    print("=" * 85)

    if eligible:
        print(
            f"{'Rank':<6}{'ID':<12}{'Name':<20}"
            f"{'Aggregate':<14}{'Attendance':<14}{'Income':<15}"
        )
        print("-" * 85)

        for rank, a in enumerate(eligible, start=1):
            print(
                f"{rank:<6}{a['id']:<12}{a['name']:<20}"
                f"{a['aggregate']:<14.2f}"
                f"{a['attendance']:<14.2f}"
                f"{a['income']:<15.2f}"
            )
    else:
        print("No applicants meet all eligibility criteria.")

    # Display rejected applicants
    print("\n--- INELIGIBLE APPLICANTS ---")

    if rejected:
        for a in rejected:
            print(
                f"{a['name']} ({a['id']}): "
                f"{a['status']} | Aggregate: {a['aggregate']:.2f}%"
            )
    else:
        print("No ineligible applicants.")

    print("\nEligibility Criteria:")
    print(f"Minimum aggregate: {MIN_AGGREGATE}%")
    print(f"Minimum subject marks: {MIN_SUBJECT_MARK}")
    print(f"Minimum attendance: {MIN_ATTENDANCE}%")
    print(f"Maximum family income: Rs. {MAX_FAMILY_INCOME}")
    print("Tie-break order: Aggregate > Attendance > Lower income > Student ID")


if __name__ == "__main__":
    main()
