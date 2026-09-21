from opensearchpy import OpenSearch
import json
import datetime


def create_client(host, username, password):
    """Create an OpenSearch client."""
    client = OpenSearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=(username, password),
        use_ssl=True,
        verify_certs=True
    )
    return client


def index_security_event(client, doc):
    """Index a security event document."""
    index_name = f'fintrust-security-{datetime.date.today().strftime("%Y-%m")}'
    response = client.index(index=index_name, body=doc)
    print(f'Indexed document: {response["_id"]} in {index_name}')
    return response['_id']


def search_high_risk_events(client, min_risk_score=80):
    """Search for high-risk events."""
    index_name = f'fintrust-security-{datetime.date.today().strftime("%Y-%m")}'
    query = {'query': {'range': {'risk_score': {'gte': min_risk_score}}}}

    try:
        results = client.search(index=index_name, body=query)
        hits = results['hits']['hits']
        print(f'Found {len(hits)} high-risk events')
        for hit in hits:
            print(f'  {hit["_source"]}')
        return hits
    except Exception as e:
        print(f'Search error: {e}')
        return []


def main():
    print("=" * 60)
    print("FINTRIST BANK - OPENSEARCH CLIENT")
    print("=" * 60)
    print()

    # Replace with your actual OpenSearch endpoint
    HOST = 'search-fintrust-security-logs.af-south-1.es.amazonaws.com'
    USERNAME = 'admin'
    PASSWORD = 'CHANGE_ME'

    try:
        client = create_client(HOST, USERNAME, PASSWORD)

        # Index a security event document
        doc = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'event_type': 'SUSPICIOUS_LOGIN',
            'account_id': 'ACC-0001',
            'source_ip': '41.13.45.22',
            'country': 'NG',
            'risk_score': 87
        }

        index_security_event(client, doc)

        # Search for high-risk events
        search_high_risk_events(client, 80)

    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: This requires a running OpenSearch cluster.")
        print("If you don't have one, the script will fail.")


if __name__ == "__main__":
    main()