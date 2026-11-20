from __future__ import annotations
from CanBeShipped import CanBeShipped
from discount_strategy import (BulkDiscount, DiscountStrategy, NoDiscount,
                               PercentageDiscount, StudentDiscount)
from input_helpers import get_int, get_non_negative_int, get_positive_float, get_positive_int
from inventory import Inventory
from order import Order
from product_factory import ProductFactory
from supplier import Supplier
import json

DATA_FILE = "inventory.json"

inventory = Inventory()
suppliers: dict[str, Supplier] = {}
orders: list[Order] = []

DISCOUNT_OPTIONS = {
    "1": ("No discount", lambda: NoDiscount()),
    "2": ("10% off", lambda: PercentageDiscount(10)),
    "3": ("$20 off orders of $200 or more", lambda: BulkDiscount(200, 20)),
    "4": ("Student discount (5% off)", lambda: StudentDiscount()),
}

def make_discount(choice: str) -> DiscountStrategy:
    _, build = DISCOUNT_OPTIONS.get(choice, DISCOUNT_OPTIONS["1"])
    return build()

def load_inventory():
    try:
        with open("DATA_FILE", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return
    for item in data.get("suppliers", []):
        supplier = Supplier(item["supplier_id"], item["name"], item["contact_email"])
        suppliers[supplier.get_supplier_id()] = supplier

    for item in data.get("products", []):
        try:
            supplier = suppliers[item["supplier_id"]]
            product = ProductFactory.create(
                item["type"], item["product_id"], item["name"], item["price"],
                item["stock"], supplier,
                weight=item.get("weight", 0.0),
                download_size=item.get("download_size", 0.0))
        except KeyError as missing:
            print(f"Skipped product {item.get('product_id', '?')}: missing {missing}.")
            continue
        except ValueError as error:
            print(f"Skipped product {item.get('product_id', '?')}: {error}")
            continue
        inventory.add_product(product)


def save_to_json():
    data = {
        "suppliers": [s.to_dict() for s in suppliers.values()],
        "products": [p.to_dict() for p in inventory.get_products()],
    }
    with open("inventory.json", "w") as file:
        json.dump(data, file, indent=4)

def choose_supplier() -> Supplier:
    supplier_id = input("Enter Supplier ID: ").strip()
    if supplier_id in suppliers:
        print(f"Using existing supplier: {suppliers[supplier_id].get_name()}")
        return suppliers[supplier_id]
    name = input("New supplier - enter name: ")
    email = input("Enter contact email: ")
    supplier = Supplier(supplier_id, name, email)
    suppliers[supplier_id] = supplier
    return supplier

def add_product():
    p_type = input("Is it a physical or digital product? (p/d): ").lower()
    if p_type != "p" and p_type != "d":
        print("Please enter p or d.")
        return

    product_id = input("Enter Product ID: ").strip()
    if inventory.find_product(product_id):
        print("That product ID already exists.")
        return

    name = input("Enter Product Name: ")
    price = float(input("Enter Product Price: "))
    stock = int(input("Enter Product Stock: "))
    supplier = choose_supplier()
    if p_type == "p":
        weight = get_positive_float("Enter Weight (kg): ")
        product = ProductFactory.create("physical", product_id, name, price, stock,
                                        supplier, weight=weight)
    else:
        size = get_positive_float("Enter Download Size (MB): ")
        product = ProductFactory.create("digital", product_id, name, price, stock,
                                        supplier, download_size=size)

    inventory.add_product(product)
    save_to_json()
    print("Product added successfully!")


def search_product():
    search_id = input("Enter Product ID to search: ").strip()
    product = inventory.find_product(search_id)

    if product:
        product.display_information()
        print(product.get_fulfilment_info())
        if isinstance(product, CanBeShipped):
            print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    else:
        print("Product not found.")


def update_stock():
    update_id = input("Enter Product ID to update stock: ").strip()
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

def choose_discount() -> DiscountStrategy:
    print("Discount:")
    for key, (label, _) in DISCOUNT_OPTIONS.items():
        print(f"  {key}. {label}")
    while True:
        choice = input("Choose a discount (1-4): ").strip()
        if choice in DISCOUNT_OPTIONS:
            return make_discount(choice)
        print("Please enter a number from 1 to 4.")

def create_order() -> None:
    order_id = input("Enter Order ID: ").strip()
    order = Order(order_id)
 
    
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
    print("5. Remove Product")
    print("6. Create Order")
    print("7. View Orders")
    print("8. Exit")
    choice = input("Enter your choice (1-8): ")

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
