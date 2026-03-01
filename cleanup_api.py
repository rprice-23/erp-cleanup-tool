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


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/clean")
async def clean_file(file: UploadFile = File(...)):

    try:
        # Save uploaded file
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"File saved: {input_path}")

        # Read Excel file
        df = pd.read_excel(input_path)

        print("Columns found:")
        print(df.columns.tolist())

        # Normalize column names
        df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")

        print("Normalized columns:")
        print(df.columns.tolist())

        # Verify required columns exist
        required = ["item_number", "description", "warehouse", "quantity"]

        for col in required:
            if col not in df.columns:
                raise Exception(f"Missing required column: {col}")

        # Clean data
        cleaned_df = df.groupby(
            ["item_number", "description", "warehouse"],
            as_index=False
        )["quantity"].sum()

        output_path = os.path.join(UPLOAD_FOLDER, "cleaned_inventory.xlsx")

        cleaned_df.to_excel(output_path, index=False)

        print("File cleaned successfully")

        return FileResponse(
            path=output_path,
            filename="cleaned_inventory.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        print("ERROR OCCURRED:")
        print(str(e))
        return {"error": str(e)}
