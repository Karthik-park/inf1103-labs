from __future__ import annotations

from product import Product


class Inventory:

    def __init__(self):
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> None:
        self.__products.append(product)

    def remove_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def get_products(self) -> list[Product]:
        return list(self.__products)

    def display_all_products(self) -> None:
        if not self.__products:
            print("Inventory is empty.")
            return
        for product in self.__products:
            product.display_information()
            print(product.get_fulfilment_info())
            print("-" * 20)
