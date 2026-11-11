
from CanBeShipped import CanBeShipped
from supplier import Supplier
from product import Product


class PhysicalProduct(Product, CanBeShipped):

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier, weight: float):
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = weight

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