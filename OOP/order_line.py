from __future__ import annotations
 
from product import Product
 
 
class OrderLine:


    def __init__(self, product: Product, quantity: int):
        
        self.__product: Product = product
        self.__quantity: int = quantity
 
    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity
 
    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity
 
    def display_information(self) -> None:
        name = self.__product.get_name()
        print(f"{name} x {self.__quantity} = ${self.calculate_subtotal():.2f}")

    