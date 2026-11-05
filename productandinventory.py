from abc import ABC, abstractmethod


class CanBeShipped(ABC):

    @abstractmethod
    def calculate_shipping_cost(self):
        pass


class Product(ABC):

    def __init__(self, productid, name, price, stock):
        self.__productid = productid
        self.__name = name
        self.__price = price
        self.__stock = stock

    def get_productid(self):
        return self.__productid

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def update_stock(self, quantity):
        self.__stock += quantity

    def display_information(self):
        print(f"Product ID: {self.__productid}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock} units")

    # used when saving to the json file
    def to_dict(self):
        return {
            "productid": self.__productid,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }

    @abstractmethod
    def get_fulfilment_info(self):
        pass


class PhysicalProduct(Product, CanBeShipped):

    def __init__(self, productid, name, price, stock, weight):
        super().__init__(productid, name, price, stock)
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight} kg")

    # $0.50 per kg
    def calculate_shipping_cost(self):
        return self.__weight * 0.5

    def get_fulfilment_info(self):
        return f"Physical Product: {self.get_name()}, Weight: {self.__weight} kg"

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data


class DigitalProduct(Product):

    def __init__(self, productid, name, price, stock, file_size):
        super().__init__(productid, name, price, stock)
        self.__download_size = file_size

    def get_download_size(self):
        return self.__download_size

    def display_information(self):
        super().display_information()
        print(f"Download Size: {self.__download_size} MB")

    def get_fulfilment_info(self):
        return "This product is a digital download and does not require shipping."

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data


class Inventory:

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        self.__products.append(product)

    def get_products(self):
        return list(self.__products)

    def find_product(self, productid):
        for product in self.__products:
            if product.get_productid() == productid:
                return product
        return None

    def display_inventory(self):
        for product in self.__products:
            product.display_information()
            print(product.get_fulfilment_info())
            print("-" * 20)