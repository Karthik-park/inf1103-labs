import json
import os 
INVENTORY_FILE = "inventory.json"

def load_inventory():
    """Load inventory.json if it exists, otherwise start with an empty inventory."""
    if os.path.exists(INVENTORY_FILE):
        try:
            with open(INVENTORY_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            print("Could not read inventory.json. Starting with an empty inventory.")
    return []

def save_inventory(inventory):
    """Save the inventory list to inventory.json."""
    with open(INVENTORY_FILE, "w") as f:
        json.dump(inventory, f, indent=4)
    print("\nInventory saved to " + INVENTORY_FILE)

def get_valid_number(prompt, number_type):
    """Ask until the user enters a valid, non-negative number."""
    while True:
        entry = input(prompt)
        try:
            value = number_type(entry)
        except ValueError:
            print("Invalid number entered. Try again.")
            continue
        if value < 0:
            print("No negative numbers. Try again.")
            continue
        return value
    
def display_all(inventory):
    print("\nInventory:\n")
    if not inventory:
        print("Inventory is empty.")
        return
    for product in inventory:
        print(f"ID: {product['id']}, Name: {product['name']}, "
              f"Price: {product['price']:.2f}, Stock: {product['stock']}")



def add_product(inventory):
    print("\nAdd New Product")
    product_id = get_valid_number("\nProduct ID: ", int)
 
    for product in inventory:
        if product["id"] == product_id:
            print("\nA product with that ID already exists.")
            return
 
    product_name = input("\nProduct Name: ").strip()
    if not product_name:
        print("\nName cannot be empty.")
        return
    product_price = get_valid_number("\nProduct Price: ", float)
    stock_quantity = get_valid_number("\nStock Quantity: ", int)
 
    inventory.append({
        "id": product_id,
        "name": product_name,
        "price": product_price,
        "stock": stock_quantity,
    })
    print("\nProduct added successfully!")

def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = get_valid_number("\nEnter Product ID: ", int)
 
    for product in inventory:
        if product["id"] == product_id:
            product["stock"] = get_valid_number("\nNew Stock Quantity: ", int)
            print("\nStock updated successfully!")
            return
    print("\nProduct not found.")
    
def search_product(inventory):
    print("\nSearch Product")
    keyword = input("\nEnter Product ID or Name: ").strip().lower()
 
    found = False
    for product in inventory:
        if keyword == str(product["id"]) or keyword in product["name"].lower():
            print(f"\nProduct Found: ID: {product['id']}, Name: {product['name']}, "
                  f"Price: {product['price']:.2f}, Stock: {product['stock']}")
            found = True
    if not found:
        print("\nProduct not found.")
 

def show_menu():
    print("\n===== Inventory Menu =====")
    print("1. Display")
    print("2. Add")
    print("3. Update")
    print("4. Search")
    print("5. Save")
    print("6. Exit")


# Main program
inventory = load_inventory()
 
# Starter products (at least three) so a first run isn't empty.
# Only used when no inventory.json exists yet.
if not inventory:
    inventory = [
        {"id": 1, "name": "Laptop", "price": 999.99, "stock": 10},
        {"id": 2, "name": "Mouse", "price": 19.99, "stock": 50},
        {"id": 3, "name": "Keyboard", "price": 49.50, "stock": 30},
    ]
    print("No saved inventory found. Loaded starter products.")
 
while True:
    show_menu()
    choice = input("\nChoose an option (1-6): ").strip()
 
    if choice == "1":
        display_all(inventory)
    elif choice == "2":
        add_product(inventory)
    elif choice == "3":
        update_stock(inventory)
    elif choice == "4":
        search_product(inventory)
    elif choice == "5":
        save_inventory(inventory)
    elif choice == "6":
        save_choice = input("\nSave before exiting? (y/n): ").strip().lower()
        if save_choice == "y":
            save_inventory(inventory)
        print("\nGoodbye!")
        break
    else:
        print("\nInvalid choice. Please enter a number from 1 to 6.")
 