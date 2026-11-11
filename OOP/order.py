from __future__ import annotations
 
from order_line import OrderLine
from product import Product

class Order:
 
    def __init__(self, order_id: str):
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
 
    def get_order_id(self) -> str:
        return self.__order_id
 
    def add_order_line(self, product: Product, quantity: int) -> None:
       
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        for line in self.__order_lines:
            if line.get_product().get_product_id() == product_id:
                self.__order_lines.remove(line)
                return True
        return False  
 
    def get_order_lines(self) -> list[OrderLine]:
        
        return list(self.__order_lines)