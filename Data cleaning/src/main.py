"""Command-line entry point for the cleaning workflow."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.cleaner import clean_dataframe
from src.report import write_excel_report, write_summary_chart


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean a CSV or Excel file and create an Excel report.")
    parser.add_argument("--input", type=Path, default=PROJECT_ROOT / "data" / "sample_dirty_data.csv", help="Input .csv or .xlsx file")
    parser.add_argument("--sheet", default=0, help="Excel sheet name or zero-based index (default: first sheet)")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "output" / "cleaned_report.xlsx", help="Output Excel workbook")
    return parser.parse_args()


def read_input(path: Path, sheet: str | int) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".xlsx", ".xls"}:
        selected_sheet: str | int = int(sheet) if str(sheet).isdigit() else sheet
        return pd.read_excel(path, sheet_name=selected_sheet)
    raise ValueError("Unsupported input format. Use .csv, .xlsx, or .xls.")


def main() -> None:
    args = parse_args()
    try:
        raw = read_input(args.input, args.sheet)
        cleaned, summary = clean_dataframe(raw)
        output_path = args.output.expanduser().resolve()
        write_excel_report(cleaned, summary, output_path)
        chart_path = output_path.parent / "cleaning_summary.png"
        write_summary_chart(summary, chart_path)
    except (FileNotFoundError, ValueError, OSError, ImportError) as exc:
        raise SystemExit(f"Error: {exc}") from exc

    print(f"Input: {args.input.resolve()}")
    print(f"Cleaned workbook: {output_path}")
    print(f"Chart: {chart_path}")
    print(f"Rows: {summary['rows_before']} -> {summary['rows_after']} | duplicates removed: {summary['duplicates_removed']}")


if __name__ == "__main__":
    main()
