from __future__ import annotations
from abc import ABC, abstractmethod

class Supplier:

    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self.__supplier_id = supplier_id
        self.__name = name
        self.__contact_email = contact_email

    def get_supplier_id(self) -> str:
        return self.__supplier_id

    def get_name(self) -> str:
        return self.__name

    def get_contact_email(self) -> str:
        return self.__contact_email

    def display_information(self) -> None:
        print(f"Supplier ID: {self.__supplier_id}")
        print(f"Supplier Name: {self.__name}")
        print(f"Contact Email: {self.__contact_email}")

    def to_dict(self) -> dict:
        return {
            "supplier_id": self.__supplier_id,
            "name": self.__name,
            "contact_email": self.__contact_email,
        }
    
class CanBeShipped(ABC):

    @abstractmethod
    def calculate_shipping_cost(self):
        pass


class Product(ABC):

    def __init__(self, product_id: str, name: str, price: float,
                     stock: int, supplier: Supplier):
            self.__product_id = product_id
            self.__name = name
            self.__price = price
            self.__stock = stock
            self.__supplier: Supplier = supplier

    def get_product_id(self) -> str:
        return self.__productid

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def get_supplier(self) -> Supplier:
            return self.__supplier

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

