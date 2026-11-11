from product import Product
from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from inventory import Inventory
from order import Order
from supplier import Supplier
import json


inventory = Inventory()
suppliers: dict[str, Supplier] = {}
orders: list[Order] = []


def load_inventory():
    try:
        with open("inventory.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return
    for item in data.get("suppliers", []):
        supplier = Supplier(item["supplier_id"], item["name"], item["contact_email"])
        suppliers[supplier.get_supplier_id()] = supplier

    for item in data:
        if item.get("type") == "physical":
            product = PhysicalProduct(item["productid"], item["name"], item["price"],
                                      item["stock"], item["weight"])
        elif item.get("type") == "digital":
            product = DigitalProduct(item["productid"], item["name"], item["price"],
                                     item["stock"], item["download_size"])
        else:
            continue
        inventory.add_product(product)


def save_to_json():
    data = {
        "suppliers": [s.to_dict() for s in suppliers.values()],
        "products": [p.to_dict() for p in inventory.get_products()],
    }
    with open("inventory.json", "w") as file:
        json.dump(data, file, indent=4)


def add_product():
    p_type = input("Is it a physical or digital product? (p/d): ").lower()
    if p_type != "p" and p_type != "d":
        print("Please enter p or d.")
        return

    product_id = int(input("Enter Product ID: "))
    if inventory.find_product(product_id):
        print("That product ID already exists.")
        return

    name = input("Enter Product Name: ")
    price = float(input("Enter Product Price: "))
    stock = int(input("Enter Product Stock: "))

    if p_type == "p":
        weight = float(input("Enter Weight (kg): "))
        product = PhysicalProduct(product_id, name, price, stock, weight)
    else:
        size = float(input("Enter Download Size (MB): "))
        product = DigitalProduct(product_id, name, price, stock, size)

    inventory.add_product(product)
    save_to_json()
    print("Product added successfully!")


def search_product():
    search_id = int(input("Enter Product ID to search: "))
    product = inventory.find_product(search_id)

    if product:
        product.display_information()
        print(product.get_fulfilment_info())
        if isinstance(product, PhysicalProduct):
            print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    else:
        print("Product not found.")


def update_stock():
    update_id = int(input("Enter Product ID to update stock: "))
    product = inventory.find_product(update_id)

    if product:
        amount = int(input("Enter amount to add (negative to remove): "))
        product.update_stock(amount)
        save_to_json()
        print(f"Stock updated! It now has {product.get_stock()} units.")
    else:
        print("Product not found.")

def remove_product():
    remove_id = input("Enter Product ID to remove: ").strip()
    product = inventory.remove_product(remove_id)
 
    if product is None:
        print("Product not found.")
        return
 
    save_to_json()
    print(f"{product.get_name()} removed from the inventory.")

def create_order() -> None:
    order_id = input("Enter Order ID: ").strip()
    order = Order(order_id)
 
    # keep adding items until the user just presses enter
    while True:
        product_id = input("Enter Product ID to add (blank to finish): ").strip()
        if product_id == "":
            break
 
        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue
 
        quantity = int(input("Enter quantity: "))
        order.add_order_line(product, quantity)
 
    orders.append(order)
    order.display_order()

def show_orders() -> None:
    if not orders:
        print("No orders yet.")
        return
 
    for order in orders:
        order.display_order()
        print("-" * 20)
load_inventory()

while True:
    print("\nWelcome to the Inventory Management System")
    print("========================================")
    print("1. Add Product")
    print("2. Search Product")
    print("3. Update Stock")
    print("4. Display Inventory")
    print("5. Exit")
    choice = input("Enter your choice (1-5): ")

    try:
        if choice == "1":
            add_product()
        elif choice == "2":
            search_product()
        elif choice == "3":
            update_stock()
        elif choice == "4":
            inventory.display_all_products()      # display_inventory() doesn't exist
        elif choice == "5":
            remove_product()
        elif choice == "6":
            create_order()
        elif choice == "7":
            show_orders()
        elif choice == "8":
            print("Exiting the Inventory Management System.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
    except ValueError:
        print("That's not a valid number, try again.")
