from datetime import datetime, timedelta
import math

# Parking rates per hour (in rupees)
VEHICLE_RATES = {
    "bike": 20,
    "car": 50,
    "bus": 100
}

# Maximum parking fee charged per 24-hour period
DAILY_LIMITS = {
    "bike": 200,
    "car": 500,
    "bus": 1000
}

# Additional penalties
LOST_TICKET_PENALTY = 200
OVERNIGHT_SURCHARGE = 100
MAX_PARKING_DAYS = 30


def calculate_parking_fee(entry, exit_time, vehicle):
    """Calculate parking fee, overnight charges, and penalties."""

    if exit_time <= entry:
        raise ValueError("Exit time must be later than entry time.")

    duration = exit_time - entry
    total_minutes = duration.total_seconds() / 60

    # Charge every started hour as one hour
    charged_hours = math.ceil(total_minutes / 60)

    # Calculate complete or partial 24-hour periods
    parking_days = math.ceil(total_minutes / (24 * 60))

    hourly_rate = VEHICLE_RATES[vehicle]
    daily_limit = DAILY_LIMITS[vehicle]

    # Calculate fee separately for each 24-hour period
    remaining_hours = charged_hours
    parking_fee = 0

    for day in range(parking_days):
        hours_today = min(remaining_hours, 24)
        daily_fee = hours_today * hourly_rate
        parking_fee += min(daily_fee, daily_limit)
        remaining_hours -= hours_today

    # Overnight surcharge applies if parking crosses midnight
    overnight = entry.date() != exit_time.date()
    overnight_fee = (
        OVERNIGHT_SURCHARGE * (exit_time.date() - entry.date()).days
    )

    # Lost ticket penalty
    lost_ticket = input("Was the parking ticket lost? (yes/no): ").strip().lower()

    if lost_ticket not in ("yes", "no"):
        raise ValueError("Enter yes or no for lost ticket.")

    penalty = LOST_TICKET_PENALTY if lost_ticket == "yes" else 0

    if total_minutes > MAX_PARKING_DAYS * 24 * 60:
        raise ValueError("Parking duration exceeds the 30-day limit.")

    total = parking_fee + overnight_fee + penalty

    return {
        "duration": duration,
        "charged_hours": charged_hours,
        "parking_days": parking_days,
        "parking_fee": parking_fee,
        "overnight_fee": overnight_fee,
        "penalty": penalty,
        "total": total
    }


def main():
    print("=" * 55)
    print("        SMART PARKING FEE MANAGEMENT")
    print("=" * 55)

    try:
        vehicle = input(
            "Enter vehicle category (bike/car/bus): "
        ).strip().lower()

        if vehicle not in VEHICLE_RATES:
            print("Invalid vehicle category.")
            return

        entry_text = input(
            "Enter entry date and time (DD-MM-YYYY HH:MM): "
        )
        exit_text = input(
            "Enter exit date and time (DD-MM-YYYY HH:MM): "
        )

        # Validate date and time format
        entry = datetime.strptime(entry_text, "%d-%m-%Y %H:%M")
        exit_time = datetime.strptime(exit_text, "%d-%m-%Y %H:%M")

        result = calculate_parking_fee(entry, exit_time, vehicle)

        print("\n" + "=" * 55)
        print("                PARKING RECEIPT")
        print("=" * 55)
        print(f"Vehicle Category : {vehicle.title()}")
        print(f"Entry Time       : {entry.strftime('%d-%m-%Y %H:%M')}")
        print(f"Exit Time        : {exit_time.strftime('%d-%m-%Y %H:%M')}")
        print(f"Parking Duration : {result['duration']}")
        print(f"Charged Hours    : {result['charged_hours']}")
        print(f"Parking Days     : {result['parking_days']}")
        print("-" * 55)
        print(f"Parking Fee      : Rs. {result['parking_fee']:.2f}")
        print(f"Overnight Charge : Rs. {result['overnight_fee']:.2f}")
        print(f"Penalty          : Rs. {result['penalty']:.2f}")
        print("-" * 55)
        print(f"TOTAL AMOUNT     : Rs. {result['total']:.2f}")
        print("=" * 55)
        print("Thank you for using our parking facility!")

    except ValueError as error:
        print("Input error:", error)


if __name__ == "__main__":
    main()
