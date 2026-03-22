import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd

# ---------------------------
# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Ensure uploads folder exists
os.makedirs(UPLOADS_DIR, exist_ok=True)

# ---------------------------
# FastAPI setup
app = FastAPI(title="ERP Cleanup Dashboard")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Only mount static if folder exists
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ---------------------------
# Helper functions


def get_files():
    """Return list of Excel/CSV files in uploads"""
    try:
        return [
            f for f in os.listdir(UPLOADS_DIR)
            if f.endswith((".xlsx", ".xls", ".csv"))
        ]
    except Exception:
        return []


def load_file(file_name):
    """Load dataframe safely"""
    file_path = os.path.join(UPLOADS_DIR, file_name)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_name} not found")

    if file_name.endswith(".csv"):
        return pd.read_csv(file_path)
    else:
        return pd.read_excel(file_path)


def load_preview(file_name):
    """Return HTML table preview"""
    try:
        df = load_file(file_name)
        return df.head(10).to_html(classes="table table-striped", index=False)
    except Exception as e:
        return f"<p style='color:red;'>Error loading preview: {e}</p>"


def get_summary_stats(file_name):
    """Generate summary statistics"""
    try:
        df = load_file(file_name)

        return {
            "total_rows": int(len(df)),
            "total_columns": int(len(df.columns)),
            "missing_values": int(df.isnull().sum().sum()),
            "duplicate_rows": int(df.duplicated().sum())
        }

    except Exception as e:
        return {
            "total_rows": 0,
            "total_columns": 0,
            "missing_values": 0,
            "duplicate_rows": 0,
            "error": str(e)
        }

# ---------------------------
# Routes


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    files = get_files()

    selected_file = files[0] if files else None

    preview_data = load_preview(
        selected_file) if selected_file else "<p>No files available</p>"
    stats = get_summary_stats(selected_file) if selected_file else {}

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "files": files,
            "preview_data": preview_data,
            "selected_file": selected_file,
            "stats": stats
        }
    )


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_alias(request: Request):
    return await dashboard(request)


@app.post("/", response_class=HTMLResponse)
async def dashboard_post(request: Request, selected_file: str = Form(...)):
    files = get_files()

    preview_data = load_preview(selected_file)
    stats = get_summary_stats(selected_file)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "files": files,
            "preview_data": preview_data,
            "selected_file": selected_file,
            "stats": stats
        }
    )

# ---------------------------
# Run server

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
