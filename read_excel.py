import pandas as pd

# Step 1: Read Excel file
df = pd.read_excel("inventory.xlsx")

print("\n=== ORIGINAL DATA ===")
print(df)


# Step 2: Standardize column names (very important in ERP cleanup)
df.columns = df.columns.str.lower().str.strip()

print("\n=== CLEANED COLUMN NAMES ===")
print(df.columns)


# Step 3: Clean description field
df["description"] = df["description"].str.lower().str.strip()

print("\n=== CLEANED DESCRIPTIONS ===")
print(df)


# Step 4: Find duplicate item numbers
duplicates = df[df.duplicated("item_number", keep=False)]

print("\n=== DUPLICATE ITEMS ===")
print(duplicates)


# Step 5: Calculate total quantity per item
totals = df.groupby("item_number")["quantity"].sum().reset_index()

print("\n=== TOTAL QUANTITY PER ITEM ===")
print(totals)


# Step 6: Export cleaned file
df.to_excel("inventory_cleaned.xlsx", index=False)

print("\n=== CLEANED FILE EXPORTED ===")
