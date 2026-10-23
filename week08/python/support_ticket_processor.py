import boto3
import json

sqs = boto3.client('sqs', region_name='af-south-1')
comp = boto3.client('comprehend', region_name='af-south-1')

# Replace ACCOUNT_ID with your actual AWS account ID
URGENT_QUEUE_URL = 'https://sqs.af-south-1.amazonaws.com/471116064922/fintrust-support-urgent'
STANDARD_QUEUE_URL = 'https://sqs.af-south-1.amazonaws.com/471116064922/fintrust-support-standard'


def redact_pii(text):
    """Detect and redact PII from text."""
    response = comp.detect_pii_entities(Text=text, LanguageCode='en')
    entities = response['Entities']

    entities.sort(key=lambda e: e['BeginOffset'], reverse=True)
    detected_types = list({e['Type'] for e in entities})
    text_chars = list(text)

    for entity in entities:
        replacement = f'[{entity["Type"]}]'
        text_chars[entity['BeginOffset']:entity['EndOffset']] = list(replacement)

    return ''.join(text_chars), detected_types


def process_support_ticket(ticket_text):
    """
    Process a support ticket:
    1. Redact PII
    2. Detect sentiment
    3. Route to appropriate queue
    """
    # Step 1: Redact PII
    redacted_text, pii_types = redact_pii(ticket_text)

    # Step 2: Detect sentiment
    sentiment_resp = comp.detect_sentiment(Text=ticket_text, LanguageCode='en')
    sentiment = sentiment_resp['Sentiment']

    # Step 3: Route to appropriate queue
    queue_url = URGENT_QUEUE_URL if sentiment == 'NEGATIVE' else STANDARD_QUEUE_URL

    message = {
        'redacted_text': redacted_text,
        'sentiment': sentiment,
        'pii_types_found': pii_types,
        'priority': 'HIGH' if sentiment == 'NEGATIVE' else 'STANDARD'
    }

    # Send to SQS
    try:
        sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message))
        message['routed_to'] = queue_url
    except Exception as e:
        message['routed_to'] = f'ERROR: {e}'

    return message


def main():
    print("=" * 60)
    print("FINTRIST BANK - SUPPORT TICKET PROCESSOR")
    print("=" * 60)
    print()

    # Test tickets
    tickets = [
        "My name is Sipho Nkosi and my account number is ACC-7823041. My ID number is 9203045678082. I contacted you from 083 555 1234. Please help me reset my PIN.",
        "This is unacceptable! I have been waiting for 3 days and no one has helped me. My account ACC-1234567 is still blocked. I am very frustrated!",
        "Hi, I just wanted to check my balance. My account is ACC-9876543."
    ]

    for i, ticket in enumerate(tickets, 1):
        print(f"Ticket {i}:")
        print(f"  {ticket[:80]}...")
        print()

        try:
            result = process_support_ticket(ticket)
            print(f"  Sentiment: {result['sentiment']}")
            print(f"  Priority: {result['priority']}")
            print(f"  PII found: {result['pii_types_found']}")
            print(f"  Redacted: {result['redacted_text'][:80]}...")
            print(f"  Routed to: {result['routed_to']}")
        except Exception as e:
            print(f"  Error: {e}")

        print()
        print("-" * 60)
        print()


if __name__ == "__main__":
    main()