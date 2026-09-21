# Week 7 Day 1 - Python APIs with Flask and FastAPI

## Framework Comparison

| Feature | Flask | FastAPI |
|---------|-------|---------|
| Type annotations | Optional | Required |
| Data validation | Manual | Automatic (Pydantic) |
| Auto docs | No | Built-in (/docs, /redoc) |
| Async support | Basic | Native async/await |
| Performance | Good | Faster (ASGI) |
| Learning curve | Lower | Moderate |
| Best for | Prototypes, simple APIs | Production APIs |

## Flask App Structure

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)