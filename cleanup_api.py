
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os
import glob
import re
import shutil
import pandas as pd
from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

# -----------------------
# Setup
# -----------------------
app = FastAPI(title="ERP Cleanup API")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
TEMPLATE_FOLDER = os.path.join(BASE_DIR, "templates")

# cleanup_api.py
import os
import re
import shutil
import pandas as pd

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

# -------------------------------
# APP AND FOLDERS
# -------------------------------
app = FastAPI()
(Add core ERP cleanup tool updates)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


templates = Jinja2Templates(directory=TEMPLATE_FOLDER)

# -----------------------
# Column mapping
# -----------------------
COLUMN_MAP = {
    "item_number": ["item number", "item_number", "item no", "sku", "part number", "product code", "material"],
    "description": ["description", "desc", "item description", "product description", "item name", "name"],
    "warehouse": ["warehouse", "wh", "whse", "location", "warehouse code", "site", "stock location"],
    "quantity": ["qty", "quantity", "quantity on hand", "on hand", "stock qty", "inventory", "balance"]
}

# -----------------------
# Helper functions
# -----------------------


def clean_column_name(col):

templates = Jinja2Templates(directory="templates")

# -------------------------------
# COLUMN MAPPING
# -------------------------------
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

# -------------------------------
# COLUMN CLEANING FUNCTIONS
# -------------------------------


def clean_column_name(col):
    """Normalize column names aggressively."""
(Add core ERP cleanup tool updates)
    col = str(col).strip().lower()
    col = re.sub(r'[^a-z0-9]', ' ', col)
    col = re.sub(r'\s+', ' ', col).strip()
    return col


def detect_header_row(df: pd.DataFrame):
    for i in range(min(20, len(df))):
        row = df.iloc[i].astype(str).str.lower().fillna("").tolist()
        if any("item" in c for c in row) and any("qty" in c or "quantity" in c for c in row):
            return i
    return None


def normalize_columns(df: pd.DataFrame, mapping: dict = None):
    df.columns = [clean_column_name(c) for c in df.columns]
    detected_mapping = {}
    for col in df.columns:
        for std_name, possibilities in COLUMN_MAP.items():
            cleaned_possibilities = [
                clean_column_name(p) for p in possibilities]
            if any(p in col for p in cleaned_possibilities):
                detected_mapping[col] = std_name

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names and map to standard ERP columns."""
    cleaned_columns = {c: clean_column_name(c) for c in df.columns}
    df = df.rename(columns=cleaned_columns)

    detected_mapping = {}
    for col in df.columns:
        for standard_name, possible_names in COLUMN_MAP.items():
            possible_cleaned = [clean_column_name(x) for x in possible_names]
            if col in possible_cleaned and standard_name not in detected_mapping.values():
                detected_mapping[col] = standard_name
(Add core ERP cleanup tool updates)
                break
    if mapping:
        for k, v in mapping.items():
            if v in df.columns:
                detected_mapping[v] = k
    df = df.rename(columns=detected_mapping)
    return df, detected_mapping



def cleanup_dataframe(df: pd.DataFrame):
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
    df = df[df["item_number"].notna()]
    grouped = df.groupby(["item_number", "description", "warehouse"], as_index=False)[
        "quantity"].sum()
    return grouped


    missing = [col for col in COLUMN_MAP if col not in df.columns]
    if missing:
        raise ValueError(
            f"Missing required columns: {missing}. Found columns: {list(df.columns)}")
(Add core ERP cleanup tool updates)

def read_file(file_path: str):
    if file_path.lower().endswith(".csv"):
        raw_df = pd.read_csv(file_path, header=None)
    else:
        raw_df = pd.read_excel(file_path, header=None)
    header_row = detect_header_row(raw_df)
    if header_row is not None:
        if file_path.lower().endswith(".csv"):
            df = pd.read_csv(file_path, header=header_row)
        else:
            df = pd.read_excel(file_path, header=header_row)
    else:
        df = raw_df.copy()
        df.columns = [f"col_{i}" for i in range(df.shape[1])]
    return df


# -----------------------
# API Routes
# -----------------------


def cleanup_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Perform cleanup logic safely."""
    df = normalize_columns(df)
    cleaned_df = df.groupby(
        ["item_number", "description", "warehouse"],
        as_index=False
    )["quantity"].sum()
    return cleaned_df
(Add core ERP cleanup tool updates)

# -------------------------------
# CUSTOM JINJA FILTERS
# -------------------------------


@app.get("/")
def home():
    return {"message": "Inventory Cleanup API is running"}


@app.post("/clean")
async def clean_file(file: UploadFile = File(...), mapping_json: str = Form(None)):
    import json
    mapping = json.loads(mapping_json) if mapping_json else None
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    df = read_file(input_path)
    df, detected_mapping = normalize_columns(df, mapping=mapping)
    required = ["item_number", "quantity"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        return JSONResponse(status_code=200, content={
            "error": "Missing required columns, manual mapping needed",
            "columns_detected": df.columns.tolist(),
            "missing": missing
        })
    if "description" not in df.columns:
        df["description"] = df["item_number"]
    if "warehouse" not in df.columns:
        df["warehouse"] = "MAIN"
    cleaned_df = cleanup_dataframe(df)
    if cleaned_df.empty:
        return JSONResponse(status_code=400, content={"error": "No usable data found"})
    output_path = os.path.join(UPLOAD_FOLDER, f"cleaned_{file.filename}")
    cleaned_df.to_excel(output_path, index=False)
    return FileResponse(
        path=output_path,
        filename=f"cleaned_{file.filename}",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# -----------------------
# Dashboard Routes
# -----------------------


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    """Serve the dashboard HTML"""
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/dashboard/data")
def dashboard_data(warehouse: str = "ALL"):
    """Return latest cleaned inventory data as JSON"""
    try:
        files = glob.glob(os.path.join(UPLOAD_FOLDER, "cleaned_*.xlsx"))
        if not files:
            fallback = os.path.join(UPLOAD_FOLDER, "inventory.xlsx")
            if os.path.exists(fallback):
                df = pd.read_excel(fallback)
            else:
                return []
        else:
            latest_file = max(files, key=os.path.getctime)
            df = pd.read_excel(latest_file)
        if warehouse != "ALL" and "warehouse" in df.columns:
            df = df[df["warehouse"] == warehouse]
        return df.fillna("").to_dict(orient="records")
    except Exception as e:
        return []


@app.get("/dashboard/files")
def list_files():
    """Return list of available cleaned files"""
    files = glob.glob(os.path.join(UPLOAD_FOLDER, "cleaned_*.xlsx"))
    files.sort(key=os.path.getctime, reverse=True)
    return [{"name": os.path.basename(f)} for f in files]


@app.get("/dashboard/compare")
def compare_files(file1: str, file2: str):
    """Compare two cleaned files"""
    try:
        path1 = os.path.join(UPLOAD_FOLDER, file1)
        path2 = os.path.join(UPLOAD_FOLDER, file2)
        df1 = pd.read_excel(path1)
        df2 = pd.read_excel(path2)
        merged = pd.merge(df1, df2, on=[
                          "item_number", "description", "warehouse"], how="outer", suffixes=("_old", "_new")).fillna(0)
        merged["quantity_change"] = merged["quantity_new"] - \
            merged["quantity_old"]
        return merged.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

# -----------------------
# Temporary Test Route
# -----------------------


app = FastAPI()


@app.get("/test")
def test():
    return {"status": "server working"}


def extract_warehouses(df: pd.DataFrame):
    """Return sorted unique warehouse names from DataFrame."""
    if "warehouse" in df.columns:
        return sorted(df["warehouse"].dropna().unique())
    return []


templates.env.filters["extract_warehouses"] = extract_warehouses

# -------------------------------
# ROUTES
# -------------------------------


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Render file upload page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/clean")
async def clean_file(file: UploadFile = File(...)):
    """Upload and clean ERP file."""
    try:
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Read file
        if file.filename.lower().endswith(".csv"):
            df = pd.read_csv(input_path)
        elif file.filename.lower().endswith((".xlsx", ".xls")):
            df = pd.read_excel(input_path)
        else:
            raise ValueError("Unsupported file type. Upload CSV or Excel.")

        cleaned_df = cleanup_dataframe(df)

        output_path = os.path.join(UPLOAD_FOLDER, f"cleaned_{file.filename}")
        cleaned_df.to_excel(output_path, index=False)

        return FileResponse(
            path=output_path,
            filename=f"cleaned_{file.filename}",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        return {"error": str(e)}


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    """Render dashboard page with latest cleaned file."""
    try:
        latest_file = max(
            [f for f in os.listdir(UPLOAD_FOLDER) if f.startswith("cleaned_")],
            key=lambda x: os.path.getctime(os.path.join(UPLOAD_FOLDER, x))
        )
        df = pd.read_excel(os.path.join(UPLOAD_FOLDER, latest_file))
    except Exception:
        df = pd.DataFrame()

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "data": df}
    )
(Add core ERP cleanup tool updates)
