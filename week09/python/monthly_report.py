import boto3
from datetime import date
from cost_explorer import get_monthly_spend_by_service

s3 = boto3.client('s3')
BUCKET = 'fintrust-cost-reports'

def generate_report():
    # Using hardcoded months for example - adjust based on current date
    m1 = get_monthly_spend_by_service(2026, 7)
    m2 = get_monthly_spend_by_service(2026, 8)
    m3 = get_monthly_spend_by_service(2026, 9)
    
    if not m1 or not m2 or not m3:
        print("Missing data, cannot generate report.")
        return

    all_services = set(list(m1.keys()) + list(m2.keys()) + list(m3.keys()))
    sorted_services = sorted(
        all_services, 
        key=lambda s: (m1.get(s,0) + m2.get(s,0) + m3.get(s,0)) / 3, 
        reverse=True
    )
    
    lines = []
    lines.append("=" * 80)
    lines.append("FINTRIST BANK - 3 MONTH COST REPORT")
    lines.append("=" * 80)
    lines.append(f"{'Service':<30} {'M1':>10} {'M2':>10} {'M3':>10} {'MoM %':>10}")
    lines.append("-" * 80)
    
    for s in sorted_services[:10]:
        c1, c2, c3 = m1.get(s, 0.0), m2.get(s, 0.0), m3.get(s, 0.0)
        mom_str = f"{((c3 - c2) / c2) * 100:+.1f}%" if c2 > 0 else "N/A"
        lines.append(f"{s:<30} ${c1:>9.2f} ${c2:>9.2f} ${c3:>9.2f} {mom_str:>10}")
        
    lines.append("=" * 80)
    report_text = "\n".join(lines)
    print(report_text)
    
    today = date.today()
    key = f"{today.year}-{today.month:02d}/monthly_summary.txt"
    
    try:
        s3.put_object(Bucket=BUCKET, Key=key, Body=report_text.encode('utf-8'))
        print(f"\nReport uploaded to s3://{BUCKET}/{key}")
    except Exception as e:
        print(f"\nCould not upload to S3: {e}")

if __name__ == "__main__":
    generate_report()
