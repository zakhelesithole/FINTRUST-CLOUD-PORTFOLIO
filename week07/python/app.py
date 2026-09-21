from flask import Flask, request, jsonify
import uuid
import datetime

app = Flask(__name__)

# In-memory store (replace with DynamoDB in production)
transactions = []


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


@app.route('/transactions', methods=['POST'])
def create_transaction():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body required'}), 400

    required = ['account_id', 'amount', 'currency']
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({'error': f'Missing fields: {missing}'}), 400

    txn = {
        'id': str(uuid.uuid4()),
        'account_id': data['account_id'],
        'amount': data['amount'],
        'currency': data['currency'],
        'status': 'pending',
        'created_at': datetime.datetime.utcnow().isoformat()
    }
    transactions.append(txn)
    return jsonify(txn), 201


@app.route('/transactions', methods=['GET'])
def list_transactions():
    account_id = request.args.get('account_id')
    if account_id:
        filtered = [t for t in transactions if t['account_id'] == account_id]
        return jsonify(filtered)
    return jsonify(transactions)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
    