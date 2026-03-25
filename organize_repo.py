import os
import shutil

# 🔹 Paths
repo_root = "/Users/pricefamilymacmini/Documents/GitHub/erp-cleanup-tool"

cleanup_tool_files = [
    "app.py", "cleanup_tool.py", "cleanup_api.py", "calculator.py",
    "cleaned_output.xlsx", "duplicates_report.xlsx", "erp_inventory_test.xlsx",
    "inventory_cleaned.xlsx"
]

upload_files = [
    "cleaned_inventory.xlsx", "erp_inventory_test.xlsx", "test_inventory.xlsx", "uploaded.xlsx"
]

# 🔹 README contents
readmes = {
    "root": """# ERP & Data Projects Portfolio

This repository showcases professional projects in ERP cleanup, data analysis, dashboards, and process mapping.

## Projects
1. [Cleanup Tool](./cleanup-tool) – A web-based ERP inventory cleanup and analytics tool.
2. [ABC Analysis](./abc-analysis) – Inventory classification analysis using ABC methodology.
3. [Data Quality Dashboard](./data-quality-dashboard) – Visualizes ERP data quality metrics.
4. [Process Mapping](./process-mapping) – Documentation and scripts for workflow/process optimization.

Each project includes a README with details, instructions, and examples.
""",
    "cleanup-tool": """# ERP Cleanup Tool

A Python/FastAPI-based tool for cleaning, normalizing, and visualizing ERP inventory data.

## Features
- Upload messy ERP inventory files (CSV/XLS/XLSX)
- Automatic header detection and data normalization
- Duplicate detection and reporting
- Dashboard visualization with templates
- Export cleaned inventory files

## Structure
- app.py – Main application entry
- cleanup_tool.py – Core data cleaning functions
- cleanup_api.py – API endpoints for file upload and cleaning
- templates/ – HTML dashboard
- uploads/ – Example and cleaned data files

## Usage
1. Install dependencies:
`pip install -r requirements.txt`
2. Run the app:
`python app.py`
3. Upload your ERP file via the web interface or API.
""",
    "abc-analysis": """# ABC Analysis

Scripts and data for inventory classification using the ABC methodology.

## Purpose
- Classify inventory items based on consumption value
- Identify critical items (A/B/C)
- Support procurement and stock optimization decisions

## Structure
- inventory_tracker.py – Main ABC analysis script
- inventory.xlsx – Sample inventory data
""",
    "data-quality-dashboard": """# Data Quality Dashboard

A Python-based dashboard for visualizing ERP data quality and reporting metrics.

## Features
- Generates Excel-based data quality reports
- Tracks duplicates, missing values, and inconsistencies
- Provides visual charts for analysis

## Structure
- generate_test_file.py – Generates sample data
- data_quality_report.xlsx – Example output file
""",
    "process-mapping": """# Process Mapping

Documentation and scripts for workflow and process optimization.

## Purpose
- Document key business processes
- Provide scripts/tools to support workflow analysis
- Share visual aids for improving processes

## Structure
- lesson1.py – Example process script
- read_excel.py – Supporting script
- Python mindmap - OrgPad.pdf – Process visual map
"""
}

# 🔹 .gitignore content
gitignore_content = """# Python cache
__pycache__/
*.pyc

# Excel temp files
~$*.xlsx

# VS Code settings
.vscode/
"""

# =========================
# Create folders if missing
folders = ["cleanup-tool/uploads", "abc-analysis", "data-quality-dashboard", "process-mapping"]
for f in folders:
    path = os.path.join(repo_root, f)
    os.makedirs(path, exist_ok=True)
    print(f"Created folder: {path}")

# =========================
# Move files into cleanup-tool
for f in cleanup_tool_files:
    src = os.path.join(repo_root, f)
    dst = os.path.join(repo_root, "cleanup-tool", f)
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"Moved {f} -> cleanup-tool/")

# Move upload files
for f in upload_files:
    src = os.path.join(repo_root, f)
    dst = os.path.join(repo_root, "cleanup-tool", "uploads", f)
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"Moved {f} -> cleanup-tool/uploads/")

# =========================
# Create README.md files
for folder, content in readmes.items():
    path = os.path.join(repo_root, folder, "README.md") if folder != "root" else os.path.join(repo_root, "README.md")
    with open(path, "w") as f:
        f.write(content)
    print(f"Created README.md in {folder}")

# =========================
# Create .gitignore
with open(os.path.join(repo_root, ".gitignore"), "w") as f:
    f.write(gitignore_content)
print("Created .gitignore")

print("✅ Repo organization complete!")
