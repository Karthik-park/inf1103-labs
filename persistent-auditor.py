INVENTORY_FILE = "inventory.txt"


def load_inventory():
    """Read saved total and transaction history from the inventory file.
    If the file doesn't exist, start fresh with no error."""
    total = 0
    history = []

    try:
        with open(INVENTORY_FILE, "r") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        return total, history

    if lines:
        # First line holds the saved total
        try:
            total = int(lines[0].split(":")[1])
        except (IndexError, ValueError):
            total = 0

        # Remaining lines hold the transaction history
        for line in lines[1:]:
            try:
                history.append(int(line))
            except ValueError:
                continue

    return total, history


def save_inventory(total, history):
    """Write the final total and transaction history to the inventory file."""
    with open(INVENTORY_FILE, "w") as f:
        f.write("TOTAL:" + str(total) + "\n")
        for entry in history:
            f.write(str(entry) + "\n")


def get_valid_input():
    entry = input("Enter stock quantity: ")

    if entry == "quit":
        return "quit"

    try:
        quantity = int(entry)
    except ValueError:
        print("Invalid number entered. Try again.")
        return None

    if quantity < 0:
        print("No negative numbers. Try again.")
        return None

    return quantity


def process_delivery(current_total, new_value):
    current_total += new_value
    return current_total


def calculate_tax(amount):
    tax = amount * 0.1
    return tax


def generate_report(total_units, failed_attempts):
    print("\n--- Final Report ---")
    print("Total Units Processed: " + str(total_units))
    print("Number of Failed/Rejected Entries: " + str(failed_attempts))


# Main program
total_inventory, transaction_history = load_inventory()
failed_attempts = 0

if total_inventory or transaction_history:
    print("Loaded previous inventory. Current total: " + str(total_inventory))
else:
    print("No previous inventory found. Starting fresh.")

while True:
    result = get_valid_input()

    if result == "quit":
        break

    if result is None:
        failed_attempts += 1
        continue

    quantity = result

    if total_inventory + quantity > 500:
        print("Overstock detected. Entry rejected.")
        failed_attempts += 1
        continue

    total_inventory = process_delivery(total_inventory, quantity)
    transaction_history.append(quantity)
    tax = calculate_tax(quantity)

    print("Delivery added: " + str(quantity) + " | Tax on this delivery: " + str(round(tax, 2)))
    print("Total Inventory: " + str(total_inventory))

save_inventory(total_inventory, transaction_history)
print("Inventory successfully saved to " + INVENTORY_FILE)

generate_report(total_inventory, failed_attempts)