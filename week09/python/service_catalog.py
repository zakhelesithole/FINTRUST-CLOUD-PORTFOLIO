import boto3

sc = boto3.client('servicecatalog', region_name='af-south-1')

def list_catalog():
    """List portfolios and products from Service Catalog."""
    try:
        portfolios = sc.list_accepted_portfolio_shares().get('PortfolioDetails', [])
        own = sc.list_portfolios().get('PortfolioDetails', [])
        all_portfolios = {p['Id']: p for p in portfolios + own}

        if not all_portfolios:
            print("No Service Catalog portfolios found.")
            return

        for pid, portfolio in all_portfolios.items():
            print(f"\nPortfolio: {portfolio['DisplayName']} ({pid})")

            try:
                products = sc.search_products_as_admin(PortfolioId=pid).get('ProductViewDetails', [])
                for pv in products:
                    p = pv['ProductViewSummary']
                    print(f"  Product: {p['Name']} | Type: {p['Type']} | Owner: {p['Owner']}")
            except Exception as e:
                print(f"  Could not list products: {e}")
                
    except Exception as e:
        print(f"Error accessing Service Catalog: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("FINTRIST BANK - SERVICE CATALOG PRODUCTS")
    print("=" * 60)
    list_catalog()
