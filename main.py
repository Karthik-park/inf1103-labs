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

print("Welcome to the Inventory Management System")
print("========================================")
print("1. Add Product")
print("2. Search Product")
print("3. Update Stock")
print("4. Display Inventory")
print("5. Exit")
input_choice = input("Enter your choice (1-5): ")


while input_choice != "5":
    if input_choice == "1":
        product_id = int(input("Enter Product ID: "))
        name = input("Enter Product Name: ")
        price = float(input("Enter Product Price: "))
        stock = int(input("Enter Product Stock: "))
        product_type = input("Enter Product Type (physical/digital): ").lower()
        if product_type == "physical":
            weight = float(input("Enter Product Weight (kg): "))
            new_product = PhysicalProduct(product_id, name, price, stock, weight)
        elif product_type == "digital":
            file_size = float(input("Enter File Size (MB): "))
            new_product = DigitalProduct(product_id, name, price, stock, file_size)
        else:
            print("Invalid product type.")
            continue

        inventory.add_product(new_product)
        save_to_json()
        print("Product added successfully!")

    elif input_choice == "2":
        search_id = int(input("Enter Product ID to search: "))
        found = False
        for product in inventory._Inventory__products:
            if product._PhysicalProduct__productid == search_id:
                product.display_information()
                print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
                found = True
                break
            else:
                if product._DigitalProduct__productid == search_id:
                    product.display_information()
                    print(product.getfulfillment_info())
                    found = True
                    break
        if not found:
            print("Product not found.")

    elif input_choice == "3":
        update_id = int(input("Enter Product ID to update stock: "))
        found = False
        for product in inventory._Inventory__products:
            if product._Product__productid == update_id:
                new_stock = int(input("Enter new stock quantity: "))
                product.update_stock(new_stock)
                save_to_json()
                print("Stock updated successfully!")
                found = True
                break
        if not found:
            print("Product not found.")

    elif input_choice == "4":
        print("Inventory from JSON file:")
        inventory.display_inventory()
        with open("inventory.json", "r") as file:
            products_data = json.load(file)
            
            
            
        

    elif input_choice == "5":
        print("Exiting the Inventory Management System.")

    else:
        print("Invalid choice. Please enter a number between 1 and 5.")

    print("Welcome to the Inventory Management System")
    print("========================================")
    print("1. Add Product")
    print("2. Search Product")
    print("3. Update Stock")
    print("4. Display Inventory")
    print("5. Exit")
    input_choice = input("Enter your choice (1-5): ")