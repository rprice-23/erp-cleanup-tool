<<<<<<< HEAD
import os
import pandas as pd


def run_cleanup(input_path, output_dir):
    print("\n=== ERP CLEANUP TOOL v2 STARTED ===")
    print("Loading file:", input_path)

    # Load Excel
    try:
        df = pd.read_excel(input_path)
    except Exception as e:
        print("Error loading file:", e)
        return

    print("Original record count:", len(df))

    # Step 1: Standardize column names
    df.columns = df.columns.str.lower().str.strip()

    # Step 2: Standardize item numbers
    df["item_number"] = df["item_number"].astype(str).str.upper().str.strip()

    # Step 3: Clean descriptions
    df["description"] = df["description"].astype(str).str.lower().str.strip()

    # Step 4: Handle missing descriptions
    missing_descriptions = df[df["description"] == "nan"]
    print("Missing descriptions found:", len(missing_descriptions))
    df["description"] = df["description"].replace("nan", "missing description")

    # Step 5: Handle missing item numbers
    missing_items = df[df["item_number"] == "NAN"]
    print("Missing item numbers found:", len(missing_items))

    # Step 6: Handle invalid quantities
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    invalid_quantities = df[df["quantity"].isna()]
    print("Invalid quantities found:", len(invalid_quantities))
    df["quantity"] = df["quantity"].fillna(0)

    # Step 7: Detect duplicates
    duplicates = df[df.duplicated("item_number", keep=False)]
    print("Duplicate records found:", len(duplicates))

    # Step 8: Combine duplicates
    cleaned_df = df.groupby(
        ["item_number", "description", "warehouse"],
        as_index=False
    )["quantity"].sum()
    print("Cleaned record count:", len(cleaned_df))

    # Step 9: Data quality report
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

    # Output paths
    cleaned_path = os.path.join(output_dir, "inventory_cleaned.xlsx")
    duplicates_path = os.path.join(output_dir, "duplicates_report.xlsx")
    report_path = os.path.join(output_dir, "data_quality_report.xlsx")

    # Export files
    cleaned_df.to_excel(cleaned_path, index=False)
    duplicates.to_excel(duplicates_path, index=False)
    quality_report.to_excel(report_path, index=False)

    print("\nFiles created:")
    print(cleaned_path)
    print(duplicates_path)
    print(report_path)
    print("\n=== CLEANUP COMPLETE ===")

    return {
        "cleaned_file": cleaned_path,
        "duplicates_file": duplicates_path,
        "report_file": report_path
    }


# ---------------------------
# AUTO-RUN: scan uploads/ folder
if __name__ == "__main__":
    import sys

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
    print("BASE_DIR:", BASE_DIR)
    print("UPLOADS_DIR exists?", os.path.exists(UPLOADS_DIR))

    # List files in base dir
    print("Files in BASE_DIR:", os.listdir(BASE_DIR))

    # List Excel files in uploads/
    try:
        excel_files = [f for f in os.listdir(
            UPLOADS_DIR) if f.lower().endswith((".xlsx", ".xls"))]
        print("Excel files found in uploads/:", excel_files)
    except Exception as e:
        print("Error accessing uploads/:", e)
        sys.exit(1)

    if not excel_files:
        print("No Excel files to process")
    else:
        test_file = os.path.join(UPLOADS_DIR, excel_files[0])
        print("Processing file:", test_file)
        run_cleanup(test_file, BASE_DIR)
=======
>>>>>>> 57d8483 (Add core ERP cleanup tool updates)
