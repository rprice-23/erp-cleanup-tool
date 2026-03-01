product = "bolt"
quantity = 120
reorder_point = 150

if quantity < reorder_point:
    print(f"reorder {product}")
else:
    print(f"{product} stock is sufficient")
    