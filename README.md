# RiskGuard Fraud API 🚨

A production-ready fraud detection backend built with FastAPI, PostgreSQL, and Machine Learning (XGBoost).

This system analyzes financial transactions in real-time using a combination of:
- Machine Learning (fraud probability)
- Behavioral rules (velocity, amount, time-gap)
- Risk scoring engine

---

## 🔥 Features

- ✅ Real-time fraud prediction (XGBoost + calibrated probabilities)
- ✅ Hybrid decision system (ML + rule-based risk scoring)
- ✅ Transaction velocity detection (rapid activity tracking)
- ✅ Time-gap fraud analysis
- ✅ Rate limiting (transaction count + amount control)
- ✅ JWT Authentication (secure user access)
- ✅ PostgreSQL database integration
- ✅ Dockerized deployment (ready for AWS EC2)

---

## 🧠 How It Works

### 1. Transaction Input
User submits:
- Amount
- Time (auto-generated)
- PCA features (V1–V28)

### 2. ML Prediction
Model returns fraud probability:
```

0.0001 → low risk
0.01   → medium risk
0.1+   → high risk

```

### 3. Risk Engine
System calculates:
- ML risk score
- Transaction amount risk
- Velocity (transactions per minute)
- Time-gap between transactions

### 4. Final Decision
| Score | Decision |
|------|---------|
| ≥ 90 | REJECTED |
| ≥ 50 | REVIEW |
| < 50 | APPROVED |

---

## 🏗️ Tech Stack

- **Backend:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Auth:** JWT (OAuth2)
- **ML Model:** XGBoost + Scikit-learn
- **Containerization:** Docker
- **Deployment:** AWS EC2

---

## 📁 Project Structure

```

.
├── router/
│   ├── auth.py
│   ├── transaction.py
├── models.py
├── schemas.py
├── db.py
├── auth.py
├── model_v2.pkl
├── features.pkl
├── Dockerfile
├── docker-compose.yml
└── main.py

````

---

## 🚀 Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/SVChaithanya/riskguard-fraud-api.git
cd riskguard-fraud-api
````

### 2. Run with Docker

```bash
docker-compose up --build
```

App runs at:

```
http://localhost:8000
```

---

## 🔐 API Endpoints

### Auth

* `POST /auth/register`
* `POST /auth/login`

### Transactions

* `POST /transactions/` → Create transaction
* `GET /transactions/history` → View history

---

## 📊 Example Response

```json
{
  "transaction_id": "uuid",
  "amount": 21900,
  "time_gap_sec": 5,
  "fraud_probability": 0.017,
  "decision": "REVIEW"
}
```

---

## ⚠️ Key Insights

* Fraud probability is **very low (0.001–0.02)** due to dataset imbalance
* Decision is **NOT based only on ML**
* Rule engine is critical for realistic fraud detection

---

## 🧪 Model Performance

* ROC-AUC: **0.98+**
* Highly imbalanced dataset handled using:

  * `scale_pos_weight`
  * Probability calibration

---

## 🛠️ Future Improvements

* Redis-based rate limiting (distributed)
* Real-time streaming (Kafka)
* Dashboard (React + charts)
* Multi-bank risk scoring system
* Model retraining pipeline

---

## 👨‍💻 Author

**Surya (SVChaithanya)**
Backend Developer | ML Systems Builder

---
