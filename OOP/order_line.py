from __future__ import annotations
 
from product import Product
 
 
class OrderLine:


    def __init__(self, product: Product, quantity: int):
        
        self.__product: Product = product
        self.__quantity: int = quantity
 
    def get_product(self) -> Product:
        return self.__product

    