from abc import ABC, abstractmethod

class CanBeShipped  (ABC):

    @abstractmethod
    def calculate_shipping_cost(self):
        pass

class Product(ABC):

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

    @abstractmethod
    def getfulfillment_info(self):
        pass

class PhysicalProduct(Product, CanBeShipped):

    def __init__(self, productid, name, price, stock, weight):
        super().__init__(productid, name, price, stock)
        self.__weight = weight

    def calculate_shipping_cost(self):
        return self.__weight * 0.5  # Example shipping cost calculation

    def getfulfillment_info(self):
        return f"Physical Product: {self._Product__name}, Weight: {self.__weight} kg"

class DigitalProduct(Product):

    def __init__(self, productid, name, price, stock, file_size):
        super().__init__(productid, name, price, stock)
        self.__file_size = file_size

    def display_info(self):
        return f"Digital Product: {self._Product__name}, File Size: {self.__file_size} MB"

    def getfulfillment_info(self):
        return "This product is a digital download and does not require shipping."
    
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