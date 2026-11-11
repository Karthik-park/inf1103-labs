from __future__ import annotations
from abc import ABC, abstractmethod
from supplier import Supplier





class Product(ABC):

    def __init__(self, product_id: str, name: str, price: float,
                     stock: int, supplier: Supplier):
            self.__product_id = product_id
            self.__name = name
            self.__price = price
            self.__stock = stock
            self.__supplier: Supplier = supplier

    def get_product_id(self) -> str:
        return self.__product_id

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
        print(f"Product ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock} units")
        print(f"Supplier: {self.__supplier.get_name()}")

    # used when saving to the json file
    def to_dict(self):
        return {
            "product_id": self.__productid,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier_id": self.__supplier.get_supplier_id(),
        }

    @abstractmethod
    def get_fulfilment_info(self):
        pass







