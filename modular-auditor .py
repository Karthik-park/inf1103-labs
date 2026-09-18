def get_valid_input():
    while True:
        entry = input("Enter stock quantity: ")
        if entry == "quit":
            return "quit"
        try:
            quantity = int(entry)
            if quantity < 0:
                print("No negative numbers. Try again.")
                return None
            return quantity
        except ValueError:
            print("Invalid number entered. Try again.")
            return None


def process_delivery(current_total, new_value):
    current_total += new_value
    return current_total


def calculate_tax(amount):
    tax = amount * 0.1
    return tax


def generate_report(total_units, failed_attempts):
    print("\n--- Final Report ---")
    print("Total Deliveries Processed: " + str(total_units))
    print("Number of Failed/Rejected Entries: " + str(failed_attempts))


# Main program
total_inventory = 0
deliveries_processed = 0
failed_attempts = 0

while True:
    result = get_valid_input()

    if result == "quit":
        break

    if result is None:
        failed_attempts += 1
        continue

    quantity = result
    total_inventory = process_delivery(total_inventory, quantity)
    tax = calculate_tax(quantity)
    deliveries_processed += 1

    print("Delivery added: " + str(quantity) + " | Tax on this delivery: " + str(round(tax, 2)))
    print("Total Inventory: " + str(total_inventory))

generate_report(deliveries_processed, failed_attempts)