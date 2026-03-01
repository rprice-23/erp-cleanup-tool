import pandas as pd

print("\n=== ERP CLEANUP TOOL v2 STARTED ===")

# Step 1: Read Excel file
df = pd.read_excel("inventory.xlsx")

print("\nOriginal record count:", len(df))


# Step 2: Standardize column names
df.columns = df.columns.str.lower().str.strip()


# Step 3: Standardize item numbers
df["item_number"] = df["item_number"].astype(str).str.upper().str.strip()


# Step 4: Clean descriptions
df["description"] = df["description"].astype(str).str.lower().str.strip()


# Step 5: Handle missing descriptions
missing_descriptions = df[df["description"] == "nan"]

print("Missing descriptions found:", len(missing_descriptions))

df["description"] = df["description"].replace("nan", "missing description")


# Step 6: Handle missing item numbers
missing_items = df[df["item_number"] == "NAN"]

print("Missing item numbers found:", len(missing_items))


# Step 7: Handle invalid quantities
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

invalid_quantities = df[df["quantity"].isna()]

print("Invalid quantities found:", len(invalid_quantities))


# Step 8: Replace invalid quantities with 0
df["quantity"] = df["quantity"].fillna(0)


# Step 9: Detect duplicates
duplicates = df[df.duplicated("item_number", keep=False)]

print("Duplicate records found:", len(duplicates))


# Step 10: Combine duplicates
cleaned_df = df.groupby(
    ["item_number", "description", "warehouse"],
    as_index=False
)["quantity"].sum()


print("Cleaned record count:", len(cleaned_df))


# Step 11: Create data quality report
quality_report = pd.DataFrame({
    "Metric": [
        "Original Records",
        "Cleaned Records",
        "Duplicate Records",
        "Missing Descriptions",
        "Invalid Quantities"
    ],
    "Count": [
        len(df),
        len(cleaned_df),
        len(duplicates),
        len(missing_descriptions),
        len(invalid_quantities)
    ]
})


# Step 12: Export files
cleaned_df.to_excel("inventory_cleaned.xlsx", index=False)
duplicates.to_excel("duplicates_report.xlsx", index=False)
quality_report.to_excel("data_quality_report.xlsx", index=False)


print("\nFiles created:")
print("inventory_cleaned.xlsx")
print("duplicates_report.xlsx")
print("data_quality_report.xlsx")

print("\n=== CLEANUP COMPLETE ===")
