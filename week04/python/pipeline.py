# ============================================
# pipeline.py
# FinTrust Bank - CSV to SQLite to Dashboard Pipeline
# Week 4 Day 3 - Cloud to Solutions Accelerator
#
# This pipeline reads a transaction CSV file, validates each row,
# loads valid rows into a SQLite database, and generates a daily
# operations report. Invalid rows are logged and skipped.
# ============================================

import csv
import sqlite3
from datetime import datetime
from pathlib import Path

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

CSV_FILE = Path("../data/transactions.csv")
DB_FILE = Path("../data/fintrust_analytics.db")
REPORT_FILE = Path("../data/daily_report.txt")

VALID_TYPES = {"TRANSFER", "DEPOSIT", "WITHDRAWAL"}
VALID_STATUSES = {"COMPLETED", "FAILED", "PENDING"}


# -------------------------------------------------------------------
# Phase 1: Read and Validate CSV
# -------------------------------------------------------------------

def validate_row(row):
    """Return (True, None) if valid, (False, reason) if invalid."""
    if not row["account_from"].strip():
        return False, "missing account_from"

    try:
        amount = float(row["amount"])
    except (ValueError, TypeError):
        return False, f"invalid amount: {row['amount']!r}"

    if amount <= 0:
        return False, f"amount must be positive, got {amount}"

    if row["type"] not in VALID_TYPES:
        return False, f"unknown type: {row['type']!r}"

    if row["status"] not in VALID_STATUSES:
        return False, f"unknown status: {row['status']!r}"

    return True, None


def load_csv(filepath):
    """Read the CSV and return (valid_rows, invalid_rows)."""
    valid = []
    invalid = []

    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ok, reason = validate_row(row)
            if ok:
                valid.append(row)
            else:
                invalid.append({"row": row, "reason": reason})

    return valid, invalid


# -------------------------------------------------------------------
# Phase 2: Load into SQLite
# -------------------------------------------------------------------

def setup_database(db_path):
    """Create the transactions table if it doesn't exist. Return a connection."""
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            account_from   TEXT NOT NULL,
            account_to     TEXT,
            amount         REAL NOT NULL,
            currency       TEXT NOT NULL,
            type           TEXT NOT NULL,
            status         TEXT NOT NULL,
            timestamp      TEXT,
            loaded_at      TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def insert_transactions(conn, valid_rows):
    """Insert valid rows. Skip rows already in the database (duplicate IDs)."""
    loaded_at = datetime.now().isoformat(timespec="seconds")
    inserted = 0
    skipped = 0

    for row in valid_rows:
        try:
            conn.execute(
                """
                INSERT INTO transactions
                    (transaction_id, account_from, account_to, amount,
                     currency, type, status, timestamp, loaded_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row["transaction_id"],
                    row["account_from"],
                    row["account_to"] or None,
                    float(row["amount"]),
                    row["currency"],
                    row["type"],
                    row["status"],
                    row["timestamp"],
                    loaded_at,
                )
            )
            inserted += 1
        except sqlite3.IntegrityError:
            skipped += 1

    conn.commit()
    return inserted, skipped


# -------------------------------------------------------------------
# Phase 3: Query and Generate Report
# -------------------------------------------------------------------

def generate_report(conn, report_path):
    """Query the DB and write a formatted daily report."""
    lines = []
    lines.append("=" * 60)
    lines.append("FINTRUST DAILY TRANSACTION REPORT")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 60)

    # Query 1: Summary totals
    row = conn.execute("""
        SELECT
            COUNT(*)                          AS total_count,
            ROUND(SUM(amount), 2)             AS total_volume,
            ROUND(AVG(amount), 2)             AS avg_amount,
            ROUND(MIN(amount), 2)             AS min_amount,
            ROUND(MAX(amount), 2)             AS max_amount
        FROM transactions
    """).fetchone()

    lines.append("\n-- SUMMARY ----------------------------------------------")
    lines.append(f"  Total transactions : {row[0]}")
    lines.append(f"  Total volume       : ZAR {row[1]:,.2f}")
    lines.append(f"  Average amount     : ZAR {row[2]:,.2f}")
    lines.append(f"  Min / Max          : ZAR {row[3]:,.2f} / ZAR {row[4]:,.2f}")

    # Query 2: Breakdown by type
    lines.append("\n-- BREAKDOWN BY TYPE ------------------------------------")
    rows = conn.execute("""
        SELECT type, COUNT(*) AS cnt, ROUND(SUM(amount), 2) AS volume
        FROM transactions
        GROUP BY type
        ORDER BY volume DESC
    """).fetchall()
    for r in rows:
        lines.append(f"  {r[0]:<12}  {r[1]:>3} txns   ZAR {r[2]:>10,.2f}")

    # Query 3: Breakdown by status
    lines.append("\n-- BREAKDOWN BY STATUS ----------------------------------")
    rows = conn.execute("""
        SELECT status, COUNT(*) AS cnt, ROUND(SUM(amount), 2) AS volume
        FROM transactions
        GROUP BY status
        ORDER BY cnt DESC
    """).fetchall()
    for r in rows:
        lines.append(f"  {r[0]:<12}  {r[1]:>3} txns   ZAR {r[2]:>10,.2f}")

    # Query 4: Top 3 largest transactions
    lines.append("\n-- TOP 3 LARGEST TRANSACTIONS ---------------------------")
    rows = conn.execute("""
        SELECT transaction_id, account_from, amount, type, status
        FROM transactions
        ORDER BY amount DESC
        LIMIT 3
    """).fetchall()
    for i, r in enumerate(rows, 1):
        lines.append(f"  #{i}  {r[0]}  {r[1]}  ZAR {r[2]:,.2f}  [{r[3]} / {r[4]}]")

    lines.append("\n" + "=" * 60)

    report_text = "\n".join(lines)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_text, encoding="utf-8")
    return report_text


# -------------------------------------------------------------------
# Main Pipeline
# -------------------------------------------------------------------

def main():
    print("=" * 60)
    print("FINTRIST BANK - DATA PIPELINE")
    print("=" * 60)

    # Phase 1
    print("\n[Phase 1] Loading and validating CSV...")
    if not CSV_FILE.exists():
        print(f"Error: CSV file not found at {CSV_FILE}")
        return

    valid_rows, invalid_rows = load_csv(CSV_FILE)
    print(f"  Valid rows:   {len(valid_rows)}")
    print(f"  Invalid rows: {len(invalid_rows)}")

    for entry in invalid_rows:
        txn_id = entry["row"].get("transaction_id", "?")
        print(f"    {txn_id}: {entry['reason']}")

    if not valid_rows:
        print("No valid rows to process. Exiting.")
        return

    # Phase 2
    print("\n[Phase 2] Loading into SQLite...")
    conn = setup_database(DB_FILE)
    inserted, skipped = insert_transactions(conn, valid_rows)
    print(f"  Inserted: {inserted}")
    print(f"  Skipped (duplicates): {skipped}")

    # Phase 3
    print("\n[Phase 3] Generating report...")
    report = generate_report(conn, REPORT_FILE)
    print(report)

    conn.close()
    print(f"\nReport saved to: {REPORT_FILE}")
    print("Pipeline complete.")


if __name__ == "__main__":
    main()