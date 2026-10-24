# Nested Loop Examination Seating Generator

def generate_seating(rows, cols, students, reserved_seats, alternate_seating):
    seating = []
    student_index = 0

    for r in range(rows):
        row_seats = []

        for c in range(cols):
            seat_id = f"R{r + 1}C{c + 1}"

            # Check whether the seat is reserved
            if seat_id in reserved_seats:
                row_seats.append("RESERVED")

            # Alternate seating: leave every second column empty
            elif alternate_seating and c % 2 == 1:
                row_seats.append("EMPTY")

            # Assign students to available seats
            elif student_index < len(students):
                row_seats.append(students[student_index])
                student_index += 1

            else:
                row_seats.append("EMPTY")

        seating.append(row_seats)

    return seating, student_index


def display_seating(seating):
    print("\n" + "=" * 75)
    print("                 EXAMINATION SEATING PLAN")
    print("=" * 75)

    for r, row in enumerate(seating):
        print(f"Row {r + 1}: ", end="")

        for c, student in enumerate(row):
            seat_id = f"R{r + 1}C{c + 1}"
            print(f"[{seat_id}: {student}]", end="  ")

        print()

    print("=" * 75)


def main():
    print("=" * 60)
    print("      EXAMINATION SEATING ARRANGEMENT GENERATOR")
    print("=" * 60)

    try:
        rows = int(input("Enter number of classroom rows: "))
        cols = int(input("Enter seats per row: "))

        if rows <= 0 or cols <= 0:
            print("Rows and columns must be positive.")
            return

        capacity = rows * cols
        print(f"Total classroom capacity: {capacity}")

        student_count = int(input("Enter number of students: "))

        if student_count < 0:
            print("Student count cannot be negative.")
            return

        if student_count > capacity:
            print("Error: Students exceed the classroom's fixed capacity.")
            return

        students = []

        for i in range(student_count):
            student = input(f"Enter student {i + 1} ID/name: ").strip()

            if not student:
                print("Student ID/name cannot be empty.")
                return

            if student in students:
                print("Duplicate student IDs/names are not allowed.")
                return

            students.append(student)

        reserved_count = int(input("Enter number of reserved seats: "))

        if reserved_count < 0 or reserved_count > capacity:
            print("Invalid number of reserved seats.")
            return

        reserved_seats = set()

        for i in range(reserved_count):
            seat = input(
                f"Enter reserved seat {i + 1} (e.g., R1C2): "
            ).strip().upper()

            # Validate seat format and position
            try:
                row_part, col_part = seat.split("C")
                row_number = int(row_part[1:])
                col_number = int(col_part)

                if (
                    not row_part.startswith("R")
                    or not (1 <= row_number <= rows)
                    or not (1 <= col_number <= cols)
                ):
                    print("Invalid seat position.")
                    return

                if seat in reserved_seats:
                    print("Seat already reserved.")
                    return

                reserved_seats.add(seat)

            except (ValueError, IndexError):
                print("Invalid format. Use a format like R1C2.")
                return

        alternate_input = input(
            "Enable alternate seating? (yes/no): "
        ).strip().lower()

        if alternate_input not in ("yes", "no"):
            print("Please enter yes or no.")
            return

        alternate_seating = alternate_input == "yes"

        # Calculate the number of usable seats before assigning students
        usable_seats = 0

        for r in range(rows):
            for c in range(cols):
                seat_id = f"R{r + 1}C{c + 1}"

                if seat_id not in reserved_seats:
                    if not alternate_seating or c % 2 == 0:
                        usable_seats += 1

        if student_count > usable_seats:
            print(
                f"Error: Only {usable_seats} seats are available "
                "under the selected restrictions."
            )
            return

        seating, assigned_count = generate_seating(
            rows, cols, students, reserved_seats, alternate_seating
        )

        display_seating(seating)

        print(f"Total classroom capacity : {capacity}")
        print(f"Students registered      : {student_count}")
        print(f"Students seated          : {assigned_count}")
        print(f"Reserved seats            : {len(reserved_seats)}")
        print(f"Unseated students         : {student_count - assigned_count}")

        print("\nSeat Status:")
        print("  Student name/ID = Assigned seat")
        print("  RESERVED        = Not available")
        print("  EMPTY           = Available seat")

    except ValueError:
        print("Invalid input. Please enter valid numbers.")

if __name__ == "__main__":
    main()
