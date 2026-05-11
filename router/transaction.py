from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

from db import get_db
from models import Transaction, Prediction
from schemas import TransactionCreate
from auth import get_current_user

import joblib
import pandas as pd

# ============================
# LOAD MODEL
# ============================
model = joblib.load("model_v2.pkl")
FEATURE_COLUMNS = joblib.load("features.pkl")
MODEL_VERSION = "fraud_model_v2"

router = APIRouter(prefix="/transactions", tags=["transactions"])

# ============================
# HELPERS
# ============================
def run_model(data_dict: dict):
    df = pd.DataFrame([data_dict])[FEATURE_COLUMNS]
    prob = float(model.predict_proba(df)[0][1])

    if pd.isna(prob):
        raise HTTPException(status_code=500, detail="Model failed")

    return prob


def generate_time_gap(last_txn_time, current_time):
    if last_txn_time is None:
        return 9999
    return (current_time - last_txn_time).total_seconds()


def to_naive(dt):
    if dt is not None and dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt


# ============================
# DECISION ENGINE (FINAL)
# ============================
def get_decision(prob, amount, tx_count_1m, time_gap):
    risk_score = 0

    # ML risk
    if prob >= 0.02:
        risk_score += 60
    elif prob >= 0.005:
        risk_score += 40
    elif prob >= 0.001:
        risk_score += 20

    # Amount risk
    if amount >= 40000:
        risk_score += 30
    elif amount >= 20000:
        risk_score += 15

    # Velocity risk
    if tx_count_1m >= 5:
        risk_score += 40
    elif tx_count_1m >= 3:
        risk_score += 25

    # Time-gap risk
    if time_gap <= 3:
        risk_score += 20
    elif time_gap <= 10:
        risk_score += 10

    # FINAL DECISION
    if risk_score >= 90:
        return "REJECTED", True

    if risk_score >= 50:
        return "REVIEW", True

    return "APPROVED", False


# ============================
# CREATE TRANSACTION
# ============================
@router.post("/")
def create_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")

    current_time = datetime.now(timezone.utc)

    # 🔹 LAST TRANSACTION
    last_txn = db.query(Transaction).filter(
        Transaction.user_id == current_user.id
    ).order_by(Transaction.transaction_at.desc()).first()

    last_time = last_txn.transaction_at if last_txn else None
    time_gap = generate_time_gap(to_naive(last_time), to_naive(current_time))

    # 🔹 COUNT TRANSACTIONS IN LAST 1 MIN
    one_min_ago = current_time - timedelta(minutes=1)

    tx_count_1m = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_at >= one_min_ago
    ).count()

    # 🔹 SAVE TRANSACTION
    txn = Transaction(
        user_id=current_user.id,
        amount=data.amount,
        transaction_at=current_time,
        time=int(time_gap),
        **{f"V{i}": getattr(data, f"V{i}") for i in range(1, 29)}
    )

    db.add(txn)
    db.commit()
    db.refresh(txn)

    # 🔹 MODEL INPUT
    input_data = {
        "Time": txn.time,
        "Amount": txn.amount,
        **{f"V{i}": getattr(txn, f"V{i}") for i in range(1, 29)}
    }

    prob = run_model(input_data)

    # 🔥 FINAL DECISION (FIXED)
    decision, is_fraud = get_decision(
        prob,
        txn.amount,
        tx_count_1m,
        int(time_gap)
    )

    # 🔹 SAVE PREDICTION
    pred = Prediction(
        transaction_id=txn.id,
        fraud_probability=prob,
        is_fraud=is_fraud,
        decision=decision,
        model_version=MODEL_VERSION
    )

    db.add(pred)
    db.commit()

    return {
        "transaction_id": str(txn.id),
        "amount": txn.amount,
        "time_gap_sec": int(time_gap),
        "fraud_probability": prob,
        "tx_count_1m": tx_count_1m,
        "decision": decision
    }


# ============================
# HISTORY
# ============================
@router.get("/history")
def get_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    txns = db.query(Transaction).filter(
        Transaction.user_id == current_user.id
    ).order_by(Transaction.transaction_at.asc()).all()

    if not txns:
        return []

    first_txn_time = txns[0].transaction_at
    result = []

    for txn in txns:
        pred = db.query(Prediction).filter(
            Prediction.transaction_id == txn.id
        ).order_by(Prediction.predicted_at.desc()).first()

        time_gap = (txn.transaction_at - first_txn_time).total_seconds()

        result.append({
            "transaction_id": str(txn.id),
            "amount": txn.amount,
            "time_gap_sec": int(time_gap),
            "fraud_probability": pred.fraud_probability if pred else None,
            "decision": pred.decision if pred else "UNKNOWN",
            "transaction_at": txn.transaction_at
        })

    result.reverse()
    return result