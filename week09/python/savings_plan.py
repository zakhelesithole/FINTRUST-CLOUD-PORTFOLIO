def calculate_savings_plan_savings(hourly_commitment_usd, term_years=3, discount_pct=0.66, utilisation_pct=1.0):
    effective_ondemand_hourly = hourly_commitment_usd / (1 - discount_pct)
    hours_in_period = term_years * 365 * 24
    total_sp_cost = hourly_commitment_usd * hours_in_period
    effective_hours_used = hours_in_period * utilisation_pct
    total_ondemand_cost = effective_ondemand_hourly * effective_hours_used
    total_savings = total_ondemand_cost - total_sp_cost

    return {
        'commitment_per_hour': hourly_commitment_usd,
        'total_ondemand_cost': round(total_ondemand_cost, 2),
        'total_sp_cost': round(total_sp_cost, 2),
        'total_savings_usd': round(total_savings, 2),
    }

if __name__ == "__main__":
    print("=" * 70)
    print("FINTRIST BANK - SAVINGS PLAN CALCULATOR")
    print("=" * 70)
    
    result = calculate_savings_plan_savings(hourly_commitment_usd=32.47, term_years=3)
    for k, v in result.items():
        print(f"  {k:<30} {v}")
