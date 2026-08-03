from decimal import Decimal

# FinTrust Bank — first Python script
customer_name = "Thabo Nkosi"
balance = Decimal("52750.00")
interest_rate = 0.085  # 8.5% annual

monthly_interest = balance * Decimal(str(interest_rate / 12))

print(f"Good morning, {customer_name}!")
print(f"Current balance: R {balance:,.2f}")
print(f"Monthly interest earned: R {monthly_interest:.2f}")