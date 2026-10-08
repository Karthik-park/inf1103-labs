import json
import os 
INVENTORY_FILE = "inventory.json"

def display_products(products):
    print("\nInventory:\n")
    for product_id, product_name, product_price, stock_quantity in products:
        print(f"ID: {product_id}, Name: {product_name}, Price: {product_price}, Stock: {stock_quantity}\n")

def add_product():
    print("\nAdd New Product")
    product_id = input("\nProduct ID: ")
    product_name = input("\nProduct Name: ")
    product_price = input("\nProduct Price: ")
    stock_quantity = input("\nStock Quantity: ")

    print("\nProduct added successfully!")

def find_product(products):
    print("\nSearch Product")
    product_id = input("\nEnter Product ID: ")
    for product in products:
        if product[0] == product_id:
            print(f"\nProduct Found: ID: {product[0]}, Name: {product[1]}, Price: {product[2]}, Stock: {product[3]}\n")
            return
    print("\nProduct not found.\n")

def load_inventory():    
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, "r") as f:
            return json.load(f)
    else:
        


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
