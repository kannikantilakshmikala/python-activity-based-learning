
# Courier Charge Optimization System

# Courier service configuration
COURIER_SERVICES = {
    "Standard": {
        "base_charge": 50,
        "per_kg": 20,
        "max_weight": 20,
        "max_dimension": 100,
        "zones": ["local", "regional", "national"],
        "restricted_allowed": False
    },
    "Express": {
        "base_charge": 100,
        "per_kg": 35,
        "max_weight": 15,
        "max_dimension": 80,
        "zones": ["local", "regional", "national"],
        "restricted_allowed": False
    },
    "Premium": {
        "base_charge": 150,
        "per_kg": 50,
        "max_weight": 30,
        "max_dimension": 120,
        "zones": ["local", "regional", "national"],
        "restricted_allowed": True
    }
}

# Distance zone multipliers
ZONE_MULTIPLIERS = {
    "local": 1.0,
    "regional": 1.5,
    "national": 2.0
}

# Urgency surcharge percentages
URGENCY_CHARGES = {
    "normal": 0,
    "urgent": 25,
    "same-day": 50
}


def calculate_volumetric_weight(length, width, height):
    """Calculate volumetric weight using a sample divisor."""
    return (length * width * height) / 5000


def calculate_charge(service, weight, zone, urgency):
    """Calculate delivery cost for a courier service."""
    details = COURIER_SERVICES[service]

    chargeable_weight = max(
        weight,
        calculate_volumetric_weight(
            parcel_length, parcel_width, parcel_height
        )
    )

    base_cost = (
        details["base_charge"]
        + chargeable_weight * details["per_kg"]
    )

    zone_cost = base_cost * ZONE_MULTIPLIERS[zone]
    urgency_cost = zone_cost * URGENCY_CHARGES[urgency] / 100

    return zone_cost + urgency_cost, chargeable_weight


def main():
    global parcel_length, parcel_width, parcel_height

    print("=" * 65)
    print("             COURIER CHARGE OPTIMIZATION")
    print("=" * 65)

    try:
        weight = float(input("Enter parcel weight (kg): "))
        parcel_length = float(input("Enter length (cm): "))
        parcel_width = float(input("Enter width (cm): "))
        parcel_height = float(input("Enter height (cm): "))

        if min(weight, parcel_length, parcel_width, parcel_height) <= 0:
            print("Weight and dimensions must be greater than zero.")
            return

        zone = input(
            "Enter distance zone (local/regional/national): "
        ).strip().lower()

        urgency = input(
            "Enter urgency (normal/urgent/same-day): "
        ).strip().lower()

        restricted_input = input(
            "Does the parcel contain restricted items? (yes/no): "
        ).strip().lower()

        if zone not in ZONE_MULTIPLIERS:
            print("Invalid distance zone.")
            return

        if urgency not in URGENCY_CHARGES:
            print("Invalid urgency option.")
            return

        if restricted_input not in ("yes", "no"):
            print("Enter yes or no for restricted items.")
            return

        restricted = restricted_input == "yes"

        volumetric_weight = calculate_volumetric_weight(
            parcel_length, parcel_width, parcel_height
        )
        chargeable_weight = max(weight, volumetric_weight)

        eligible_services = []
        rejected_services = []

        for service, details in COURIER_SERVICES.items():
            reasons = []

            if chargeable_weight > details["max_weight"]:
                reasons.append("exceeds weight limit")

            if max(parcel_length, parcel_width, parcel_height) > details["max_dimension"]:
                reasons.append("exceeds dimension limit")

            if zone not in details["zones"]:
                reasons.append("zone not supported")

            if restricted and not details["restricted_allowed"]:
                reasons.append("restricted items not accepted")

            if reasons:
                rejected_services.append((service, reasons))
            else:
                charge, _ = calculate_charge(
                    service, weight, zone, urgency
                )
                eligible_services.append((service, charge))

        print("\n" + "=" * 65)
        print("                  COURIER COMPARISON")
        print("=" * 65)
        print(f"Actual Weight      : {weight:.2f} kg")
        print(f"Volumetric Weight  : {volumetric_weight:.2f} kg")
        print(f"Chargeable Weight  : {chargeable_weight:.2f} kg")
        print(f"Distance Zone      : {zone.title()}")
        print(f"Urgency            : {urgency.title()}")
        print(f"Restricted Parcel  : {'Yes' if restricted else 'No'}")
        print("-" * 65)

        if eligible_services:
            print(f"{'Service':<20}{'Delivery Charge (Rs.)':>25}")
            print("-" * 65)

            for service, charge in sorted(
                eligible_services, key=lambda item: item[1]
            ):
                print(f"{service:<20}{charge:>25.2f}")

            best_service, best_charge = min(
                eligible_services, key=lambda item: item[1]
            )

            print("-" * 65)
            print(f"Recommended Service : {best_service}")
            print(f"Lowest Charge       : Rs. {best_charge:.2f}")
        else:
            print("No courier service is eligible for this parcel.")

        if rejected_services:
            print("\nINELIGIBLE SERVICES")
            for service, reasons in rejected_services:
                print(f"{service}: {', '.join(reasons)}")

        print("=" * 65)

    except ValueError:
        print("Invalid input. Please enter valid numeric values.")


if __name__ == "__main__":
    main()
