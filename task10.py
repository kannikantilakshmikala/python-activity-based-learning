# Parking fee configuration
VEHICLE_RATES = {
    "bike": 10,
    "car": 30,
    "truck": 50
}

DAILY_LIMITS = {
    "bike": 100,
    "car": 300,
    "truck": 500
}

OVERNIGHT_FEE = 50
LATE_EXIT_PENALTY = 100
MAX_PARKING_DAYS = 30


def get_valid_datetime(prompt):
    """Read and validate date and time."""
    while True:
        value = input(prompt).strip()

        try:
            return datetime.strptime(
                value, "%Y-%m-%d %H:%M"
            )
        except ValueError:
            print(
                "Invalid format! Use YYYY-MM-DD HH:MM "
                "(Example: 2026-10-24 09:30)"
            )


def calculate_parking_fee(entry, exit_time, vehicle,
                          penalty=False):
    """Calculate the total parking fee."""

    if exit_time <= entry:
        raise ValueError(
            "Exit time must be later than entry time."
        )

    duration_seconds = (exit_time - entry).total_seconds()
    total_hours = duration_seconds / 3600

    if total_hours > MAX_PARKING_DAYS * 24:
        raise ValueError(
            "Parking duration cannot exceed 30 days."
        )

    # Charge at least one hour
    charged_hours = max(1, math.ceil(total_hours))

    # Charge for each calendar day separately
    daily_charges = {}
    current_day = entry.date()

    while current_day <= exit_time.date():
        daily_charges[current_day] = 0
        current_day = current_day.fromordinal(
            current_day.toordinal() + 1
        )

    remaining_hours = charged_hours
    current_day = entry.date()

    # Allocate parking hours to calendar days
    while remaining_hours > 0:
        hours_today = min(24, remaining_hours)

        daily_charges[current_day] = min(
            hours_today * VEHICLE_RATES[vehicle],
            DAILY_LIMITS[vehicle]
        )

        remaining_hours -= hours_today
        current_day = current_day.fromordinal(
            current_day.toordinal() + 1
        )

    base_fee = sum(daily_charges.values())

    # Overnight fee: charged once per night crossed
    overnight_nights = max(
        0, (exit_time.date() - entry.date()).days
    )
    overnight_fee = overnight_nights * OVERNIGHT_FEE

    # Optional penalty
    penalty_fee = LATE_EXIT_PENALTY if penalty else 0

    total_fee = base_fee + overnight_fee + penalty_fee

    return {
        "duration": total_hours,
        "charged_hours": charged_hours,
        "base_fee": base_fee,
        "overnight_fee": overnight_fee,
        "penalty_fee": penalty_fee,
        "total_fee": total_fee
    }


def main():
    print("=" * 45)
    print(" SMART PARKING FEE MANAGEMENT SYSTEM")
    print("=" * 45)

    print("\nVehicle categories:")
    for vehicle, rate in VEHICLE_RATES.items():
        print(
            f"{vehicle.title()}: Rs.{rate}/hour "
            f"(Daily limit: Rs.{DAILY_LIMITS[vehicle]})"
        )

    # Validate vehicle category
    while True:
        vehicle = input(
            "\nEnter vehicle type (bike/car/truck): "
        ).strip().lower()

        if vehicle in VEHICLE_RATES:
            break

        print("Invalid vehicle type. Please try again.")

    entry = get_valid_datetime(
        "Enter entry time (YYYY-MM-DD HH:MM): "
    )

    while True:
        exit_time = get_valid_datetime(
            "Enter exit time (YYYY-MM-DD HH:MM): "
        )

        if exit_time > entry:
            break

        print("Exit time must be later than entry time.")

    # Ask about penalty
    while True:
        answer = input(
            "Apply late-exit penalty? (yes/no): "
        ).strip().lower()

        if answer in ("yes", "no"):
            break

        print("Please enter yes or no.")

    try:
        result = calculate_parking_fee(
            entry, exit_time, vehicle,
            penalty=(answer == "yes")
        )

        print("\n" + "=" * 45)
        print("          PARKING BILL")
        print("=" * 45)
        print(f"Vehicle type    : {vehicle.title()}")
        print(f"Entry time      : {entry}")
        print(f"Exit time       : {exit_time}")
        print(f"Duration        : {result['duration']:.2f} hours")
        print(f"Charged hours   : {result['charged_hours']}")
        print(f"Base fee        : Rs.{result['base_fee']:.2f}")
        print(f"Overnight fee   : Rs.{result['overnight_fee']:.2f}")
        print(f"Penalty         : Rs.{result['penalty_fee']:.2f}")
        print("-" * 45)
        print(f"TOTAL FEE       : Rs.{result['total_fee']:.2f}")
        print("=" * 45)

    except ValueError as error:
        print("Error:", error)


if __name__ == "__main__":
    main()
