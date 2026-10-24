from productandinventory import Product, Inventory
import json

inventory = Inventory()

print("Welcome to the Inventory Management System")
print("========================================")
print("1. Add Product")
print("2. Search Product")
print("3. Display Inventory")
print("4. Exit")
input_choice = input("Enter your choice (1-4): ")


while input_choice != "4":
    if input_choice == "1":
        product_id = int(input("Enter Product ID: "))
        name = input("Enter Product Name: ")
        price = float(input("Enter Product Price: "))
        stock = int(input("Enter Product Stock: "))
        new_product = Product(product_id, name, price, stock)
        
        inventory.add_product(new_product)
        with open ("inventory.json", "w") as file:
            json.dump(new_product,file, indent=4)
        print("Product added successfully!")

    elif input_choice == "2":
        search_id = int(input("Enter Product ID to search: "))
        found = False
        for product in inventory._Inventory__products:
            if product._Product__productid == search_id:
                product.display_information()
                found = True
                break
        if not found:
            print("Product not found.")

    elif input_choice == "3":
        inventory.display_inventory()
        with open("inventory.json", "r") as file:
            products_data = json.load(file)
            print("Inventory from JSON file:")
            print(json.dumps(products_data, indent=4))
            
        

    elif input_choice == "4":
        print("Exiting the Inventory Management System.")
    else:
        print("Invalid choice. Please enter a number between 1 and 4.")

    print("Welcome to the Inventory Management System")
    print("========================================")
    print("1. Add Product")
    print("2. Search Product")
    print("3. Display Inventory")
    print("4. Exit")
    input_choice = input("Enter your choice (1-4): ")