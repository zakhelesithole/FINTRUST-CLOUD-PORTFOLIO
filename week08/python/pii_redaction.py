import boto3

comp = boto3.client('comprehend', region_name='af-south-1')


def redact_pii(text):
    """
    Detect and redact PII from support ticket text.
    Returns redacted text and list of detected PII types.
    """
    response = comp.detect_pii_entities(Text=text, LanguageCode='en')
    entities = response['Entities']

    # Sort descending by position so replacements don't shift offsets
    entities.sort(key=lambda e: e['BeginOffset'], reverse=True)

    detected_types = list({e['Type'] for e in entities})
    text_chars = list(text)

    for entity in entities:
        replacement = f'[{entity["Type"]}]'
        text_chars[entity['BeginOffset']:entity['EndOffset']] = list(replacement)

    return ''.join(text_chars), detected_types


def analyze_sentiment(text):
    """Detect sentiment of the text."""
    response = comp.detect_sentiment(Text=text, LanguageCode='en')
    return {
        'sentiment': response['Sentiment'],
        'scores': response['SentimentScore']
    }


def main():
    print("=" * 60)
    print("FINTRIST BANK - PII REDACTION AND SENTIMENT")
    print("=" * 60)
    print()

    # Test with a sample support ticket
    ticket = (
        "My name is Sipho Nkosi and my account number is ACC-7823041. "
        "My ID number is 9203045678082. I contacted you from 083 555 1234. "
        "Please help me reset my PIN."
    )

    print("Original:")
    print(f"  {ticket}")
    print()

    try:
        # Redact PII
        redacted, pii_types = redact_pii(ticket)
        print("Redacted:")
        print(f"  {redacted}")
        print()
        print(f"PII types found: {pii_types}")
        print()

        # Sentiment analysis
        sentiment_result = analyze_sentiment(ticket)
        print(f"Sentiment: {sentiment_result['sentiment']}")
        print(f"Scores: Positive={sentiment_result['scores']['Positive']:.3f} "
              f"Negative={sentiment_result['scores']['Negative']:.3f}")

    except Exception as e:
        print(f"Error: {e}")
        print()
        print("Note: This requires Comprehend permissions.")


if __name__ == "__main__":
    main()