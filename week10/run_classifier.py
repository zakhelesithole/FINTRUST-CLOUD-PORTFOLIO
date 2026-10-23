from fintrust_migration import classify_instances

def main():
    print("=" * 60)
    print("FINTRIST BANK - MIGRATION CLASSIFIER (6Rs)")
    print("=" * 60)
    
    portfolio, untagged = classify_instances()

    print("\n=== FinTrust Migration Portfolio Summary ===")
    total = sum(len(v) for v in portfolio.values())
    
    if total == 0 and len(untagged) == 0:
        print("No EC2 instances found in this region.")
        return

    for strategy, instances in sorted(portfolio.items()):
        pct = len(instances) / total * 100 if total else 0
        print(f"{strategy.upper():12s}: {len(instances):4d} instances ({pct:.1f}%)")
        
    print(f"{'UNTAGGED':12s}: {len(untagged):4d} instances (needs classification)")
    print(f"{'TOTAL':12s}: {total + len(untagged):4d}")

if __name__ == "__main__":
    main()
