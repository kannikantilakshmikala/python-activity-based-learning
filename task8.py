# Nested Loop Calendar Generator

def generate_calendar(month, year, starting_weekday, days_in_month):
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    print("\n" + "=" * 35)
    print(f"          {month} {year}")
    print("=" * 35)

    # Print weekday headings
    for day in weekdays:
        print(f"{day:>5}", end="")
    print()

    print("-" * 35)

    # Calculate the number of blank positions before day 1
    current_position = starting_weekday

    # Indent the first date to its correct weekday
    for _ in range(starting_weekday):
        print("    ", end="")

    # Generate dates using nested loops
    date = 1

    while date <= days_in_month:
        # Print dates for one week
        for _ in range(7 - current_position):
            if date > days_in_month:
                break

            print(f"{date:>5}", end="")
            date += 1
            current_position += 1

        print()

        # Start a new week
        if current_position == 7:
            current_position = 0

    print("=" * 35)


def main():
    print("===== NESTED LOOP CALENDAR GENERATOR =====")

    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    try:
        month_number = int(input("Enter month number (1-12): "))
        year = int(input("Enter year: "))
        starting_weekday = int(
            input("Enter starting weekday (0=Mon, 1=Tue, ..., 6=Sun): ")
        )
        days_in_month = int(input("Enter number of days in the month: "))

        if not 1 <= month_number <= 12:
            print("Invalid month number.")
            return

        if year < 1:
            print("Year must be positive.")
            return

        if not 0 <= starting_weekday <= 6:
            print("Starting weekday must be between 0 and 6.")
            return

        # Determine valid month length, including leap years
        if month_number in [1, 3, 5, 7, 8, 10, 12]:
            valid_days = 31
        elif month_number in [4, 6, 9, 11]:
            valid_days = 30
        else:
            leap_year = (
                year % 400 == 0
                or (year % 4 == 0 and year % 100 != 0)
            )
            valid_days = 29 if leap_year else 28

        if days_in_month != valid_days:
            print(
                f"Invalid number of days for {months[month_number - 1]} "
                f"{year}. Expected {valid_days} days."
            )
            return

        generate_calendar(
            months[month_number - 1],
            year,
            starting_weekday,
            days_in_month
        )

    except ValueError:
        print("Invalid input. Please enter integers only.")


if __name__ == "__main__":
    main()
