from __future__ import annotations
from product import Product
from supplier import Supplier

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