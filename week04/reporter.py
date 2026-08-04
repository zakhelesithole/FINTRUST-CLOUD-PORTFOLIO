from datetime import datetime


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