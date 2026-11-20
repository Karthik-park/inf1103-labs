from __future__ import annotations

from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier

class ProductFactory:
    
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier,
               weight: float = 0.0, download_size: float = 0.0) -> Product:
        kind = product_type.strip().lower()
        if kind == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity, supplier, weight)
        elif kind == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity, supplier, download_size)
        else:
            raise ValueError(f"Unknown product type: {product_type}")