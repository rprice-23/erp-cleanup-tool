# cleanup_api.py
import re
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import shutil
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Map possible ERP column names to standard names
COLUMN_MAP = {
    "item_number": [
        "item number", "item_number", "item no", "item no.",
        "part number", "part_number", "part no", "part#",
        "sku", "product code", "product_code", "material"
    ],

    "description": [
        "description", "desc", "item description",
        "product description", "product_desc"
    ],

    "warehouse": [
        "warehouse", "wh", "whse", "warehouse code",
        "warehouse location", "location", "site"
    ],

    "quantity": [
        "qty", "quantity", "quantity on hand",
        "on hand", "onhand", "stock qty",
        "stock quantity", "inventory", "balance"
    ]
}


def clean_column_name(col):
    """Normalize column names aggressively."""

    col = str(col)

    # Remove leading/trailing whitespace
    col = col.strip()

    # Convert to lowercase
    col = col.lower()

    # Replace special characters with space
    col = re.sub(r'[^a-z0-9]', ' ', col)

    # Collapse multiple spaces
    col = re.sub(r'\s+', ' ', col)

    # Final strip
    col = col.strip()

    return col


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enterprise-grade column auto-detection.
    Handles messy ERP exports safely.
    """

    # Clean all incoming column names
    cleaned_columns = {
        original: clean_column_name(original)
        for original in df.columns
    }

    df = df.rename(columns=cleaned_columns)

    print("Cleaned column names:", cleaned_columns)

    detected_mapping = {}

    for col in df.columns:
        for standard_name, possible_names in COLUMN_MAP.items():

            possible_cleaned = [clean_column_name(x) for x in possible_names]

            if col in possible_cleaned:

                # Prevent duplicate mappings
                if standard_name not in detected_mapping.values():
                    detected_mapping[col] = standard_name

                break

    df = df.rename(columns=detected_mapping)

    print("Final detected mapping:", detected_mapping)

    missing = [col for col in COLUMN_MAP if col not in df.columns]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}. "
            f"Found columns: {list(df.columns)}. "
            f"Detected mapping: {detected_mapping}"
        )

    return df

                def cleanup_dataframe(df: pd.DataFrame) -> pd.DataFrame:
                """Perform your existing cleanup logic."""
                # Normalize column names first
                df = normalize_columns(df)

                # Drop duplicates and sum quantities
                cleaned_df = df.groupby(
        ["item_number", "description", "warehouse"],
        as_index=False
    )["quantity"].sum()

        return cleaned_df


        @ app.get("/", response_class=HTMLResponse)
        async def home(request: Request):
    """Render home page."""
        return templates.TemplateResponse("index.html", {"request": request})


        @ app.post("/clean")
        async def clean_file(file: UploadFile = File(...)):
    """Endpoint to upload and clean an ERP Excel file."""
        try:
        # Save uploaded file
        input_path= os.path.join(UPLOAD_FOLDER, file.filename)
        with open(input_path, "wb") as buffer:
    shutil.copyfileobj(file.file, buffer)
        print(f"File saved: {input_path}")

        # Read file (Excel or CSV)
    if file.filename.lower().endswith(".csv"):
        df = pd.read_csv(input_path)
    elif file.filename.lower().endswith(".xlsx") or file.filename.lower().endswith(".xls"):
        df = pd.read_excel(input_path)
    else:
        raise ValueError("Unsupported file type. Please upload CSV or Excel.")

        print("Original columns:", df.columns.tolist())

        # Clean dataframe
        cleaned_df= cleanup_dataframe(df)

        print("Cleaned columns:", cleaned_df.columns.tolist())

        # Clean dataframe
        cleaned_df= cleanup_dataframe(df)

        # Save cleaned file
        output_path= os.path.join(UPLOAD_FOLDER, f"cleaned_{file.filename}")
        cleaned_df.to_excel(output_path, index=False)
        print(f"File cleaned successfully: {output_path}")

        # Return file for download
        return FileResponse(
    path = output_path,
    filename = f"cleaned_{file.filename}",
    media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

    except Exception as e:
    print("ERROR OCCURRED:", str(e))
    return {"error": str(e)}
