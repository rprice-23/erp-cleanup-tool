import pandas as pd
import random
import numpy as np

# Realistic ERP-style column names (messy but mappable)
columns = [
    "Item No",                # item_number
    "Part Number",            # duplicate meaning
    "SKU",                    # duplicate meaning
    "Item Description",      # description
    "Desc",                  # duplicate meaning
    "WHSE",                  # warehouse
    "Warehouse Location",    # duplicate meaning
    "Qty On Hand",           # quantity
    "Quantity",              # duplicate meaning
    "On Hand",               # duplicate meaning
    "Unit Cost",
    "Extended Cost",
    "Lot Number",
    "Serial Number",
    "Supplier",
    "Supplier ID",
    "Bin Location",
    "Aisle",
    "Section",
    "Last Count Date",
    "Last Receipt Date",
    "Status",
    "Item Type",
    "UOM",
    "Notes"
]

# Sample realistic data
item_numbers = [f"ITEM-{1000+i}" for i in range(50)]
descriptions = [
    "Steel Bolt",
    "Hex Nut",
    "Flat Washer",
    "Bearing Assembly",
    "Hydraulic Pump",
    "Drive Shaft",
    "Control Valve",
    "Aluminum Plate",
    "Rubber Gasket",
    "Motor Assembly"
]

warehouses = ["MAIN", "WH1", "WH2", "WH3", "FIELD"]
suppliers = ["Grainger", "Fastenal", "McMaster", "Applied Ind.", "Motion"]

data = []

for i in range(100):

    item = random.choice(item_numbers)
    desc = random.choice(descriptions)
    wh = random.choice(warehouses)
    qty = random.randint(0, 500)

    row = {
        "Item No": item if random.random() > 0.1 else "",
        "Part Number": item if random.random() > 0.5 else "",
        "SKU": item if random.random() > 0.7 else "",
        "Item Description": desc if random.random() > 0.1 else "",
        "Desc": desc if random.random() > 0.6 else "",
        "WHSE": wh if random.random() > 0.1 else "",
        "Warehouse Location": wh if random.random() > 0.5 else "",
        "Qty On Hand": qty if random.random() > 0.1 else None,
        "Quantity": qty if random.random() > 0.6 else None,
        "On Hand": qty if random.random() > 0.7 else None,
        "Unit Cost": round(random.uniform(1, 500), 2),
        "Extended Cost": round(qty * random.uniform(1, 500), 2),
        "Lot Number": f"LOT-{random.randint(100, 999)}",
        "Serial Number": f"SN-{random.randint(10000, 99999)}",
        "Supplier": random.choice(suppliers),
        "Supplier ID": random.randint(100, 999),
        "Bin Location": f"B-{random.randint(1, 50)}",
        "Aisle": random.randint(1, 20),
        "Section": random.choice(["A", "B", "C", "D"]),
        "Last Count Date": pd.Timestamp.today() - pd.Timedelta(days=random.randint(1, 365)),
        "Last Receipt Date": pd.Timestamp.today() - pd.Timedelta(days=random.randint(1, 365)),
        "Status": random.choice(["Active", "Inactive"]),
        "Item Type": random.choice(["Raw Material", "Finished Good", "Component"]),
        "UOM": random.choice(["EA", "BOX", "PALLET"]),
        "Notes": "" if random.random() > 0.7 else "Check stock"
    }

    data.append(row)

df = pd.DataFrame(data)

# Add duplicate rows intentionally
df = pd.concat([df, df.sample(10)], ignore_index=True)

# Shuffle rows
df = df.sample(frac=1).reset_index(drop=True)

# Save file
df.to_excel("realistic_messy_inventory.xlsx", index=False)

print("Created realistic_messy_inventory.xlsx")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("Columns list:", df.columns.tolist())
