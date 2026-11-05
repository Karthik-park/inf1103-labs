from productandinventory import PhysicalProduct, DigitalProduct, Inventory
import json

inventory = Inventory()


def load_inventory():
    try:
        with open("inventory.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return

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
    data = []
    for product in inventory.get_products():
        data.append(product.to_dict())
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
            inventory.display_inventory()
        elif choice == "5":
            print("Exiting the Inventory Management System.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
    except ValueError:
        print("That's not a valid number, try again.")