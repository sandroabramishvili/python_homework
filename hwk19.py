# 1. მოცემულია ფუქცია, რომელიც პარამეტრად იღებს order-ების ლისტს,
#    order-ები არის დიქტების სახით: {"product": "apple, "quantity": 5}
#    inventory არის დიქტის სახით: {"product": stock}

#    ფუნქცია ამოწმებს ორდერში მოთხოვნილი პროდუქტი თუ არის inventory-ში, ამოწმებს თუ არის საკმარისი
#    ოდენობა და შემდეგ inventory-ში აკლებს მოთხოვნილ ოდენობას და successful_orders-ში ამატებს order-ს.

def process_orders(orders, inventory):

    successful_orders = []

    for order in orders:
        product = order["product"]
        quantity = order["quantity"]

        if product not in inventory:
            raise ValueError(f"Product '{product}' not found in inventory")

        if quantity > inventory[product]:
            raise ValueError(f"Not enough stock for '{product}'")

        inventory[product] -= quantity
        successful_orders.append(order)

    return successful_orders


# ამ ფუნქციისთვის დაწერეთ ტესტი, რომელიც შეამოწმებს
#    ა. order-ში გადმოცემული პროდუქტი არის თუ არა საწყობში
#    ბ. order-ში გადმოცემული პროდუქტის ოდენობა არის თუ არა საწყობში
#    გ. თუ ყველაფერი სწორად გადმოეცა, საბოლოოდ სწორად აკლებს თუ არა საწყობში არსებული
#       პროდუქტის ოდენობას order-ში მოთხოვნილ ოდენობას

import pytest


def test_product_not_in_inventory():
    orders = [{"product": "banana", "quantity": 1}]
    inventory = {"apple": 10}

    with pytest.raises(ValueError, match="not found in inventory"):
        process_orders(orders, inventory)


def test_quantity_exceeds_stock():
    orders = [{"product": "apple", "quantity": 5}]
    inventory = {"apple": 3}

    with pytest.raises(ValueError, match="Not enough stock"):
        process_orders(orders, inventory)


def test_successful_orders():
    orders = [
        {"product": "apple", "quantity": 5},
        {"product": "banana", "quantity": 2},
    ]
    inventory = {"apple": 10, "banana": 4}

    successful_orders = process_orders(orders, inventory)

    assert successful_orders == orders
    assert inventory == {"apple": 5, "banana": 2}