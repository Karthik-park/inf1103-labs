ORDERS_FILE = "orders.txt"


def load_inventory():
    
    orders = []

    try:
        with open(ORDERS_FILE, "r") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        return orders

    for line in lines:
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 3:
            continue
        try:
            order_id = int(parts[0])
            name = parts[1]
            quantity = int(parts[2])
        except ValueError:
            continue
        orders.append((order_id, name, quantity))

    return orders


def save_inventory(orders):
    
    with open(ORDERS_FILE, "w") as f:
        for order_id, name, quantity in orders:
            f.write(str(order_id) + "," + name + "," + str(quantity) + "\n")


def display_orders(orders):
    print("\nCurrent Orders:\n")
    for order_id, name, quantity in orders:
        print(str(order_id) + ", " + name + ", " + str(quantity))


def get_valid_quantity():
    entry = input("Enter Quantity: ")
    try:
        quantity = int(entry)
    except ValueError:
        print("Invalid number entered. Try again.")
        return None

    if quantity < 0:
        print("No negative numbers. Try again.")
        return None

    return quantity


def next_order_id(orders):
    if not orders:
        return 1001
    return max(order_id for order_id, _, _ in orders) + 1

# Main program
orders = load_inventory()
failed_attempts = 0

display_orders(orders)

while True:
    print()
    product_name = input("Enter Product Name: ")

    if product_name.lower() == "quit":
        break

    quantity = get_valid_quantity()
    if quantity is None:
        failed_attempts += 1
        continue

    order_id = next_order_id(orders)
    orders.append((order_id, product_name, quantity))

    print("\nNew Order Added:")
    print(str(order_id) + "," + product_name + "," + str(quantity))

save_inventory(orders)
print("\nOrder successfully saved to " + ORDERS_FILE)

print("\n--- Final Report ---")
print("Total Orders Processed: " + str(len(orders)))
print("Number of Failed/Rejected Entries: " + str(failed_attempts))

