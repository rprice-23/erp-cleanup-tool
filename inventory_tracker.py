inventory = {}


def add_item():
    name = input('Enter item name: ').lower()
    quantity = int(input('Enter quantity:'))

    if name in inventory:
        inventory[name] += quantity
    else:
        inventory[name] = quantity
