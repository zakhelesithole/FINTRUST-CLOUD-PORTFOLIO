from pathlib import Path
from fintrust_pipeline.loader import load_csv
from fintrust_pipeline.database import setup_database, insert_transactions
from fintrust_pipeline.reporter import generate_report

CSV_FILE = Path("data/transactions.csv")
DB_FILE = Path("data/fintrust_analytics.db")
REPORT_FILE = Path("data/daily_report.txt")


if __name__ == "__main__":
    print("=" * 60)
    print("FINTRIST BANK - DATA PIPELINE (Package Version)")
    print("=" * 60)

    # Phase 1
    print("\n[Phase 1] Loading and validating CSV...")
    if not CSV_FILE.exists():
        print(f"Error: CSV file not found at {CSV_FILE}")
        exit(1)

    valid_rows, invalid_rows = load_csv(CSV_FILE)
    print(f"  Valid rows:   {len(valid_rows)}")
    print(f"  Invalid rows: {len(invalid_rows)}")

    for entry in invalid_rows:
        txn_id = entry["row"].get("transaction_id", "?")
        print(f"    {txn_id}: {entry['reason']}")

    if not valid_rows:
        print("No valid rows to process. Exiting.")
        exit(1)

    # Phase 2
    print("\n[Phase 2] Loading into SQLite...")
    conn = setup_database(DB_FILE)
    inserted, skipped = insert_transactions(conn, valid_rows)
    print(f"  Inserted: {inserted}")
    print(f"  Skipped (duplicates): {skipped}")

    # Phase 3
    print("\n[Phase 3] Generating report...")
    generate_report(conn, REPORT_FILE)

    conn.close()
    print(f"\nReport saved to: {REPORT_FILE}")
    print("Pipeline complete.")