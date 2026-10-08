# Excel Data Cleaning and Reporting

A small Python project inspired by the linked Excel data-cleaning tutorial. It imports a CSV or Excel worksheet, trims and standardizes text, normalizes column names, removes duplicate rows, handles blank values, and writes a formatted Excel report.

## What it does

- Accepts `.csv`, `.xlsx`, or `.xls` input.
- Trims whitespace, converts empty strings to missing values, and standardizes common column names.
- Removes fully duplicated rows.
- Fills missing text values with `Unknown` and missing numeric values with the column median (or `0` when no median is available).
- Adds `Data Quality` and `Summary` sheets to the output workbook.
- Creates an `output/cleaning_summary.png` chart.
- Includes a deliberately messy sample dataset so you can run it immediately.

The cleanup rules are intentionally simple and visible in `src/cleaner.py`. Review and adjust them for your own data before relying on the results.

## Run in VS Code (Windows)

1. Open this project folder in VS Code: **File → Open Folder…**
2. Open **Terminal → New Terminal**.
3. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use the VS Code terminal's Command Prompt profile and run `.venv\Scripts\activate.bat` instead.

4. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Run the sample:

   ```powershell
   python -m src.main
   ```

   Or provide your own file and (for Excel) sheet name:

   ```powershell
   python -m src.main --input data/my_file.xlsx --sheet Sheet1 --output output/my_report.xlsx
   ```

The cleaned workbook and chart are written to `output/`. If you are using VS Code, select the `.venv` interpreter when prompted (Ctrl+Shift+P → **Python: Select Interpreter**).

## Input expectations

The first row should contain column names. The program preserves the source columns and adds normalized versions of their names, for example `Customer Name` becomes `customer_name`. Numeric columns should contain values that pandas can read as numbers. For special rules (date parsing, category mapping, domain-specific missing values), update `clean_dataframe` in `src/cleaner.py`.

## Project layout

```text
data-cleaning-reporting/
├── data/sample_dirty_data.csv
├── output/                 # generated files
├── src/
│   ├── __init__.py
│   ├── cleaner.py
│   ├── report.py
│   └── main.py
├── requirements.txt
└── README.md
```
