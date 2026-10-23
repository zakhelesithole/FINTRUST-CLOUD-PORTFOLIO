def tco_break_even(on_prem_annual_cost, aws_monthly_cost, migration_one_time_cost, onprem_inflation_pct=0.03, months=60):
    on_prem_monthly = on_prem_annual_cost / 12
    cumulative_aws = 0.0
    cumulative_on_prem = 0.0
    break_even_month = None

    for month in range(1, months + 1):
        year = (month - 1) // 12 + 1
        inflated_monthly = on_prem_monthly * ((1 + onprem_inflation_pct) ** (year - 1))
        cumulative_on_prem += inflated_monthly
        cumulative_aws += aws_monthly_cost
        if month == 1:
            cumulative_aws += migration_one_time_cost
            
        if break_even_month is None and cumulative_aws < cumulative_on_prem:
            break_even_month = month

    return break_even_month

if __name__ == "__main__":
    print("=" * 70)
    print("FINTRIST BANK - TCO BREAK-EVEN CALCULATOR")
    print("=" * 70)
    
    month = tco_break_even(4_200_000, 248_000, 850_000)
    print(f"Break-even reached in month: {month}")
