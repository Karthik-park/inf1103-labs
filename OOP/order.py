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
        # composition: the order makes its own lines,
        # you pass in a product and quantity, not a ready-made OrderLine
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)