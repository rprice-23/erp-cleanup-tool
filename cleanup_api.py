# cleanup_api.py
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
    "item_number": ["item number", "itemno", "part number", "sku", "item_number"],
    "description": ["description", "desc", "item description"],
    "warehouse": ["warehouse", "wh", "warehouse location"],
    "quantity": ["qty", "quantity", "quantity on hand", "on hand"]
}


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize ERP column names safely by merging duplicates."""

    df.columns = df.columns.str.strip()

    new_df = pd.DataFrame()

    for standard_name, variations in COLUMN_MAP.items():

        matching_cols = [
            col for col in df.columns
            if col.lower().strip() in variations
        ]

        if matching_cols:

            # Combine columns by taking first non-null value across them
            new_df[standard_name] = (
                df[matching_cols]
                .bfill(axis=1)
                .iloc[:, 0]
            )

        else:
            raise ValueError(
                f"Missing required column: {standard_name}. "
                f"Found columns: {df.columns.tolist()}"
            )

    return new_df


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


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render home page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/clean")
async def clean_file(file: UploadFile = File(...)):
    """Endpoint to upload and clean an ERP Excel file."""
    try:
        # Save uploaded file
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
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
cleaned_df = cleanup_dataframe(df)

print("Cleaned columns:", cleaned_df.columns.tolist())

# Clean dataframe
cleaned_df = cleanup_dataframe(df)

# Save cleaned file
output_path = os.path.join(UPLOAD_FOLDER, f"cleaned_{file.filename}")
cleaned_df.to_excel(output_path, index=False)
print(f"File cleaned successfully: {output_path}")

# Return file for download
return FileResponse(
    path=output_path,
    filename=f"cleaned_{file.filename}",
    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

except Exception as e:
    print("ERROR OCCURRED:", str(e))
    return {"error": str(e)}
