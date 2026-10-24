# Retail Billing with Multiple Discount Rules

# Category-specific tax rates
TAX_RATES = {
    "electronics": 18,
    "clothing": 5,
    "groceries": 0,
    "accessories": 12
}

# Discount rules based on subtotal
DISCOUNT_RULES = [
    (5000, 10),   # 10% discount for bills >= 5000
    (2000, 5),    # 5% discount for bills >= 2000
    (1000, 2)     # 2% discount for bills >= 1000
]

MAX_DISCOUNT = 1000  # Maximum discount allowed in rupees


def get_discount(subtotal):
    """Calculate discount based on threshold and maximum limit."""
    discount_rate = 0

    for threshold, rate in DISCOUNT_RULES:
        if subtotal >= threshold:
            discount_rate = rate
            break

    discount = subtotal * discount_rate / 100

    # Apply maximum concession limit
    discount = min(discount, MAX_DISCOUNT)

    return discount, discount_rate


def main():
    products = []

    print("===== RETAIL BILLING SYSTEM =====")

    try:
        count = int(input("Enter number of products: "))

        if count <= 0:
            print("Number of products must be greater than zero.")
            return

        for i in range(count):
            print(f"\nEnter details for product {i + 1}")

            name = input("Product name: ").strip()
            if not name:
                print("Product name cannot be empty.")
                return

            price = float(input("Price per unit: Rs. "))
            quantity = int(input("Quantity: "))

            print("Categories:", ", ".join(TAX_RATES.keys()))
            category = input("Enter category: ").strip().lower()

            if price < 0 or quantity <= 0:
                print("Price cannot be negative and quantity must be positive.")
                return

            if category not in TAX_RATES:
                print("Invalid category.")
                return

            amount = price * quantity
            tax_rate = TAX_RATES[category]

            products.append({
                "name": name,
                "price": price,
                "quantity": quantity,
                "category": category,
                "amount": amount,
                "tax_rate": tax_rate
            })

    except ValueError:
        print("Invalid input. Enter valid numeric values.")
        return

    # Calculate subtotal before discount
    subtotal = sum(item["amount"] for item in products)

    # Calculate threshold discount
    discount, discount_rate = get_discount(subtotal)

    # Allocate discount proportionally to each item
    total_tax = 0

    for item in products:
        item_discount = (
            item["amount"] / subtotal * discount
            if subtotal > 0 else 0
        )

        taxable_amount = item["amount"] - item_discount
        item["discount"] = item_discount
        item["tax"] = taxable_amount * item["tax_rate"] / 100
        total_tax += item["tax"]

    grand_total = subtotal - discount + total_tax

    # Print itemized invoice
    print("\n" + "=" * 90)
    print("                         RETAIL INVOICE")
    print("=" * 90)

    print(
        f"{'Product':<18}{'Qty':>5}{'Price':>12}"
        f"{'Amount':>12}{'Discount':>12}{'Tax':>10}"
    )
    print("-" * 90)

    for item in products:
        print(
            f"{item['name']:<18}"
            f"{item['quantity']:>5}"
            f"{item['price']:>12.2f}"
            f"{item['amount']:>12.2f}"
            f"{item['discount']:>12.2f}"
            f"{item['tax']:>10.2f}"
        )

    print("-" * 90)
    print(f"{'Subtotal:':<25} Rs. {subtotal:>12.2f}")
    print(
        f"{'Discount (' + str(discount_rate) + '%):':<25}"
        f" Rs. {discount:>12.2f}"
    )
    print(f"{'Maximum discount limit:':<25} Rs. {MAX_DISCOUNT:>12.2f}")
    print(f"{'Total tax:':<25} Rs. {total_tax:>12.2f}")
    print("=" * 90)
    print(f"{'GRAND TOTAL:':<25} Rs. {grand_total:>12.2f}")
    print("=" * 90)
    print("Thank you for shopping!")


if __name__ == "__main__":
    main()
