from productandinventory import PhysicalProduct, Inventory, DigitalProduct
import json

FILENAME = "inventory.json"
inventory = Inventory()

def create_product_from_dict(item):
    if item.get("type") == "physical":
        return PhysicalProduct(item["productid"], item["name"], item["price"],
                               item["stock"], item["weight"])
    elif item.get("type") == "digital":
        return DigitalProduct(item["productid"], item["name"], item["price"],
                              item["stock"], item["download_size"])
    else:
        print(f"Skipping product with unknown type: {item}")
        return None

def load_from_json():
    try:
        with open(FILENAME, "r") as file:
            for item in json.load(file):
                product = create_product_from_dict(item)
                if product is not None:
                    inventory.add_product(product)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
 
def save_to_json():
    data = [product.to_dict() for product in inventory.get_products()]
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)

def show_menu():
    print("\nWelcome to the Inventory Management System")
    print("========================================")
    print("1. Add Product")
    print("2. Search Product")
    print("3. Update Stock")
    print("4. Display Inventory")
    print("5. Exit")
    return input("Enter your choice (1-5): ")

def add_product():
    product_type = input("Physical or Digital product? (p/d): ").strip().lower()
    if product_type not in ("p", "d"):
        print("Invalid type. Please enter 'p' or 'd'.")
        return
 
    product_id = int(input("Enter Product ID: "))
    if inventory.find_product(product_id) is not None:
        print("A product with that ID already exists.")
        return
    name = input("Enter Product Name: ")
    price = float(input("Enter Product Price: "))
    stock = int(input("Enter Product Stock: "))
 
    if product_type == "p":
        weight = float(input("Enter Weight (kg): "))
        new_product = PhysicalProduct(product_id, name, price, stock, weight)
    else:
        download_size = float(input("Enter Download Size (MB): "))
        new_product = DigitalProduct(product_id, name, price, stock, download_size)
 
    inventory.add_product(new_product)
    save_to_json()
    print("Product added successfully!")

def search_product():
    search_id = int(input("Enter Product ID to search: "))
    product = inventory.find_product(search_id)
    if product is None:
        print("Product not found.")
        return
    product.display_information()
    print(product.getfulfillment_info())
    if isinstance(product, PhysicalProduct):
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
 
 
def update_stock():
    update_id = int(input("Enter Product ID to update stock: "))
    product = inventory.find_product(update_id)
    if product is None:
        print("Product not found.")
        return
    quantity = int(input("Enter quantity to add (use a negative number to remove): "))
    product.update_stock(quantity)
    save_to_json()
    print(f"Stock updated successfully! New stock: {product.get_stock()} units")

def main():
    load_from_json()
    choice = show_menu()
 
    while choice != "5":
        try:
            if choice == "1":
                add_product()
            elif choice == "2":
                search_product()
            elif choice == "3":
                update_stock()
            elif choice == "4":
                print("Current Inventory:")
                inventory.display_inventory()
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number where one is expected.")
 
        choice = show_menu()
 
    print("Exiting the Inventory Management System.")
 
 
if __name__ == "__main__":
    main()