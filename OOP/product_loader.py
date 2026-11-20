from __future__ import annotations
import csv
from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier

def load_products(path: str, inventory: Inventory, supplier: Supplier) -> int:
    loaded = 0
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)                      # skip the header row
            for line_number, row in enumerate(reader, start=2):
                if not row:
                    continue
                try:
                    product_type, product_id, name, price, stock = row
                    product = ProductFactory.create(product_type, product_id, name,
                                                    float(price), int(stock), supplier)
                except ValueError as error:
                    print(f"Skipped row {line_number} ({', '.join(row)}): {error}")
                    continue
                inventory.add_product(product)
                loaded += 1
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
    return loaded