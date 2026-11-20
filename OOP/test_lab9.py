import inspect

import pytest

import order as order_module
from digital_product import DigitalProduct
from discount_strategy import (BulkDiscount, DiscountStrategy, NoDiscount,
                               PercentageDiscount, StudentDiscount)
from input_helpers import get_positive_float
from inventory import Inventory
from order import Order
from order_line import OrderLine
from physical_product import PhysicalProduct
from product import Product
from product_factory import ProductFactory
from product_loader import load_products
from supplier import Supplier


@pytest.fixture
def supplier():
    return Supplier("S1", "Acme", "sales@acme.com")


def order_totalling_250(supplier, discount=None):
    o = Order("O1", discount)
    o.add_order_line(ProductFactory.create("physical", "P1", "Desk", 50.0, 10, supplier, weight=5), 5)
    return o




def test_order_defaults_to_no_discount(supplier):
    o = order_totalling_250(supplier)
    assert isinstance(o.get_discount(), NoDiscount)
    assert o.calculate_total() == 250


def test_bulk_then_percentage_on_the_same_order(supplier):
    o = order_totalling_250(supplier, BulkDiscount(200, 20))
    assert o.calculate_total() == 230
    o.set_discount(PercentageDiscount(10))
    assert o.calculate_total() == pytest.approx(225)


def test_bulk_discount_below_threshold_changes_nothing():
    assert BulkDiscount(200, 20).apply(199.99) == 199.99


def test_new_strategy_without_changing_order(supplier):
    class HalfPrice(DiscountStrategy):
        def apply(self, total):
            return total / 2
    o = order_totalling_250(supplier, HalfPrice())
    assert o.calculate_total() == 125
    assert order_totalling_250(supplier, StudentDiscount()).calculate_total() == pytest.approx(237.5)


def test_order_contains_no_discount_branching():
    import ast, textwrap
    source = textwrap.dedent(inspect.getsource(order_module.Order.calculate_total))
    tree = ast.parse(source)
    assert not any(isinstance(node, (ast.If, ast.IfExp, ast.Match)) for node in ast.walk(tree))


def test_discount_strategy_is_abstract():
    with pytest.raises(TypeError):
        DiscountStrategy()




def test_factory_builds_each_type(supplier):
    physical = ProductFactory.create("physical", "P1", "Lamp", 25.0, 10, supplier, weight=2)
    digital = ProductFactory.create("digital", "D1", "Editor", 49.9, 100, supplier, download_size=500)
    assert isinstance(physical, PhysicalProduct) and isinstance(physical, Product)
    assert isinstance(digital, DigitalProduct) and isinstance(digital, Product)


def test_unknown_type_raises_clear_error(supplier):
    with pytest.raises(ValueError, match="Unknown product type: service"):
        ProductFactory.create("service", "S1", "Install", 30.0, 5, supplier)


def test_main_creates_products_only_through_the_factory():
    import main
    source = inspect.getsource(main)
    assert "PhysicalProduct(" not in source
    assert "DigitalProduct(" not in source




@pytest.mark.parametrize("price", [0, -5])
def test_price_must_be_positive(supplier, price):
    with pytest.raises(ValueError, match="Price must be greater than zero"):
        ProductFactory.create("physical", "P1", "Lamp", price, 1, supplier)


def test_stock_cannot_be_negative(supplier):
    with pytest.raises(ValueError, match="Stock quantity cannot be negative"):
        ProductFactory.create("digital", "D1", "Editor", 10.0, -1, supplier)


def test_stock_update_cannot_go_below_zero(supplier):
    p = ProductFactory.create("physical", "P1", "Lamp", 25.0, 3, supplier)
    with pytest.raises(ValueError):
        p.update_stock(-4)
    assert p.get_stock() == 3


@pytest.mark.parametrize("quantity", [0, -2])
def test_order_line_quantity_must_be_positive(supplier, quantity):
    p = ProductFactory.create("physical", "P1", "Lamp", 25.0, 3, supplier)
    with pytest.raises(ValueError, match="Quantity must be greater than zero"):
        OrderLine(p, quantity)


def test_digital_product_keeps_the_stock_rule(supplier):
    # LSP: a subclass may not drop a rule its parent enforces.
    with pytest.raises(ValueError):
        DigitalProduct("D1", "Editor", 10.0, -1, supplier, 100)




def test_get_positive_float_asks_again(monkeypatch, capsys):
    answers = iter(["abc", "-5", "12.50"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))
    assert get_positive_float("Price: ") == 12.50
    out = capsys.readouterr().out.splitlines()
    assert out == ["Please enter a valid number, e.g. 12.50",
                   "Please enter a number greater than zero."]


def test_load_products_skips_bad_rows(tmp_path, supplier, capsys):
    path = tmp_path / "products.csv"
    path.write_text(
        "product_type,product_id,name,price,stock_quantity\n"
        "physical,P001,Desk Lamp,25.00,10\n"
        "digital,D001,Photo Editor,49.90,100\n"
        "service,S001,Installation,30.00,5\n"
        "physical,P002,Office Chair,abc,3\n"
        "physical,P003,Monitor Stand,39.50,7\n")
    inv = Inventory()
    assert load_products(str(path), inv, supplier) == 3
    assert [p.get_product_id() for p in inv.get_products()] == ["P001", "D001", "P003"]
    out = capsys.readouterr().out
    assert "Unknown product type: service" in out
    assert "Office Chair" in out
    assert out.strip().endswith("Load attempt finished.")


def test_missing_file_is_handled(tmp_path, supplier, capsys):
    inv = Inventory()
    assert load_products(str(tmp_path / "nope.csv"), inv, supplier) == 0
    out = capsys.readouterr().out
    assert "Products file not found" in out
    assert "Load attempt finished." in out
    assert inv.get_products() == []
