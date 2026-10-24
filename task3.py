# Employee Payroll and Deduction Analysis

# Progressive income tax slabs (example monthly rates)
# (upper limit, tax rate)
TAX_SLABS = [
    (25000, 0),    # 0% tax up to Rs. 25,000
    (50000, 5),    # 5% on the next slab
    (100000, 10),  # 10% on the next slab
    (float("inf"), 20)  # 20% above Rs. 1,00,000
]


def calculate_progressive_tax(taxable_salary):
    """Calculate tax progressively across salary slabs."""
    tax = 0
    previous_limit = 0

    for upper_limit, rate in TAX_SLABS:
        if taxable_salary <= previous_limit:
            break

        amount_in_slab = min(
            taxable_salary, upper_limit
        ) - previous_limit

        if amount_in_slab > 0:
            tax += amount_in_slab * rate / 100

        previous_limit = upper_limit

    return tax


def main():
    print("=" * 55)
    print("       EMPLOYEE PAYROLL MANAGEMENT SYSTEM")
    print("=" * 55)

    try:
        employee_id = input("Enter employee ID: ").strip()
        employee_name = input("Enter employee name: ").strip()

        if not employee_id or not employee_name:
            print("Employee ID and name cannot be empty.")
            return

        basic_pay = float(input("Enter basic pay (Rs.): "))
        hra = float(input("Enter house rent allowance (Rs.): "))
        other_allowances = float(
            input("Enter other allowances (Rs.): ")
        )
        overtime_hours = float(input("Enter overtime hours: "))
        overtime_rate = float(
            input("Enter overtime rate per hour (Rs.): ")
        )
        incentives = float(input("Enter incentives (Rs.): "))

        pf_rate = float(input("Enter PF deduction rate (%): "))
        insurance = float(input("Enter insurance deduction (Rs.): "))
        other_deductions = float(
            input("Enter other deductions (Rs.): ")
        )

        values = [
            basic_pay, hra, other_allowances, overtime_hours,
            overtime_rate, incentives, pf_rate, insurance,
            other_deductions
        ]

        if any(value < 0 for value in values):
            print("Values cannot be negative.")
            return

        if pf_rate > 100:
            print("PF rate cannot exceed 100%.")
            return

    except ValueError:
        print("Invalid input. Please enter numeric values correctly.")
        return

    # Calculate earnings
    overtime_pay = overtime_hours * overtime_rate

    gross_salary = (
        basic_pay + hra + other_allowances
        + overtime_pay + incentives
    )

    # Employee provident fund deduction
    pf_deduction = basic_pay * pf_rate / 100

    # Progressive tax based on gross salary
    income_tax = calculate_progressive_tax(gross_salary)

    # Calculate total deductions
    total_deductions = (
        pf_deduction + income_tax
        + insurance + other_deductions
    )

    net_salary = gross_salary - total_deductions

    # Display salary statement
    print("\n")
    print("=" * 60)
    print("                  SALARY STATEMENT")
    print("=" * 60)
    print(f"Employee ID   : {employee_id}")
    print(f"Employee Name : {employee_name}")
    print("-" * 60)

    print("EARNINGS")
    print(f"{'Basic Pay':<35} Rs. {basic_pay:>10,.2f}")
    print(f"{'House Rent Allowance':<35} Rs. {hra:>10,.2f}")
    print(
        f"{'Other Allowances':<35} Rs. "
        f"{other_allowances:>10,.2f}"
    )
    print(
        f"{'Overtime Pay':<35} Rs. "
        f"{overtime_pay:>10,.2f}"
    )
    print(f"{'Incentives':<35} Rs. {incentives:>10,.2f}")
    print("-" * 60)
    print(f"{'GROSS SALARY':<35} Rs. {gross_salary:>10,.2f}")

    print("\nDEDUCTIONS")
    print(
        f"{'Provident Fund':<35} Rs. "
        f"{pf_deduction:>10,.2f}"
    )
    print(
        f"{'Progressive Income Tax':<35} Rs. "
        f"{income_tax:>10,.2f}"
    )
    print(
        f"{'Insurance':<35} Rs. "
        f"{insurance:>10,.2f}"
    )
    print(
        f"{'Other Deductions':<35} Rs. "
        f"{other_deductions:>10,.2f}"
    )
    print("-" * 60)
    print(
        f"{'TOTAL DEDUCTIONS':<35} Rs. "
        f"{total_deductions:>10,.2f}"
    )
    print("=" * 60)
    print(f"{'NET SALARY':<35} Rs. {net_salary:>10,.2f}")
    print("=" * 60)


if __name__ == "__main__":
    main()
