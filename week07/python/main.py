from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, validator
from typing import Optional, List
import uuid
import datetime

app = FastAPI(title="FinTrust Transaction API", version="1.0.0")


class TransactionIn(BaseModel):
    account_id: str = Field(..., min_length=1, description="Account identifier")
    amount: float = Field(..., gt=0, description="Must be positive")
    currency: str = Field(..., regex=r'^[A-Z]{3}$', description="ISO 4217 currency code")
    description: Optional[str] = None

    @validator('amount')
    def amount_max(cls, v):
        if v > 1_000_000:
            raise ValueError('Amount exceeds single-transaction limit of 1,000,000')
        return v


class TransactionOut(TransactionIn):
    id: str
    status: str
    created_at: str


class StatusUpdate(BaseModel):
    status: str


transactions: List[dict] = []


@app.get('/health')
async def health():
    return {'status': 'ok'}


@app.post('/transactions', response_model=TransactionOut, status_code=201)
async def create_transaction(body: TransactionIn):
    txn = {
        'id': str(uuid.uuid4()),
        **body.dict(),
        'status': 'pending',
        'created_at': datetime.datetime.utcnow().isoformat()
    }
    transactions.append(txn)
    return txn


@app.get('/transactions', response_model=List[TransactionOut])
async def list_transactions(account_id: Optional[str] = Query(None)):
    if account_id:
        return [t for t in transactions if t['account_id'] == account_id]
    return transactions


@app.get('/transactions/{txn_id}', response_model=TransactionOut)
async def get_transaction(txn_id: str):
    for t in transactions:
        if t['id'] == txn_id:
            return t
    raise HTTPException(status_code=404, detail="Transaction not found")


@app.patch('/transactions/{txn_id}/status', response_model=TransactionOut)
async def update_status(txn_id: str, body: StatusUpdate):
    if body.status not in ['approved', 'rejected']:
        raise HTTPException(status_code=400, detail="Status must be 'approved' or 'rejected'")

    for t in transactions:
        if t['id'] == txn_id:
            t['status'] = body.status
            return t

    raise HTTPException(status_code=404, detail="Transaction not found")