class Product:

    def __init__(self, __productid, __name, __price, __stock):
        self.__productid = __productid
        self.__name = __name
        self.__price = __price
        self.__stock = __stock

    def update_stock(self, quantity):
        self.__stock += quantity

    def display_information(self):
        print(f"Product ID: {self.__productid}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock} units")

product1 = Product(101, "Laptop", 999.99, 10)
product1.display_information()

class Inventory:

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        self.__products.append(product)

    def display_inventory(self):
        for product in self.__products:
            product.display_information()
            print("-" * 20)