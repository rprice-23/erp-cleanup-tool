import pandas as pd
import random
from datetime import date, timedelta

# Define messy column name options for key columns
column_name_options = {
    "item_number": ["Item No", "item number", "SKU", "part number", "item_number"],
    "description": ["Description", "Desc", "item description", "descr", "Description"],
    "warehouse": ["Warehouse", "wh", "Warehouse Location", "WH", "warehouse"],
    "quantity": ["Qty", "quantity", "Qty on Hand", "On Hand", "qty"]
}

# Other random/noise column names
# 21 extra columns to reach 25 total
extra_columns = [f"Extra_Col_{i}" for i in range(1, 21)]

# Random choices for extra data
colors = ["Blue", "Red", "Green", "Yellow",
          "Black", "White", "Orange", "Purple"]
items = ["Widget", "Gizmo", "Gadget", "Thingamajig", "Doohickey"]
warehouses = ["WH-A", "WH-B", "WH-C"]
suppliers = ["ACME Corp", "WidgetWorks", "GizmoMart", "SupplyCo"]

# Build data
rows = []
for _ in range(100):
    row = {
        random.choice(column_name_options["item_number"]): 1000 + random.randint(1, 500),
        random.choice(column_name_options["description"]): f"{random.choice(colors)} {random.choice(items)}",
        random.choice(column_name_options["warehouse"]): random.choice(warehouses),
        random.choice(column_name_options["quantity"]): random.randint(1, 200),
    }
    # Add extra/noise columns
    for col in extra_columns:
        row[col] = random.choice([f"Extra_{random.randint(1, 1000)}", None])
    rows.append(row)

# Create DataFrame
df = pd.DataFrame(rows)

# Shuffle columns to make it messy
df = df.sample(frac=1, axis=1)

# Save to Excel
df.to_excel("messy_inventory.xlsx", index=False)
print("Messy inventory file created: messy_inventory.xlsx")
