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
    """Rename columns according to COLUMN_MAP and check required columns."""
    df = df.rename(
        columns={col: key for key, names in COLUMN_MAP.items()
                 for col in df.columns if col.lower() in names}
    )
    missing = [col for col in COLUMN_MAP if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
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

        # Read Excel file
        df = pd.read_excel(input_path)
        print("Columns found:", df.columns.tolist())

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
