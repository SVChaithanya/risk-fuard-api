# 🚀 RiskGuard API — Real-Time Fraud Detection Engine

RiskFuard API is a production-ready backend system for **real-time financial fraud detection**.
It combines **machine learning predictions** with **rule-based risk scoring** (amount, velocity, time-gap) to make intelligent transaction decisions.

---

## 🔥 Key Features

* ⚡ **Real-Time Fraud Detection**

  * Predicts fraud probability using trained ML model (XGBoost + calibration)

* 🧠 **Hybrid Decision Engine**

  * Combines:

    * ML probability
    * Transaction amount risk
    * Velocity (transactions per minute)
    * Time-gap behavior

* 🛡️ **Dynamic Risk Decisions**

  * APPROVED
  * REVIEW
  * REJECTED

* 📊 **Transaction History Tracking**

  * Time-based behavior analysis
  * Fraud probability monitoring

* 🔐 **Authentication System**

  * JWT-based login & secure endpoints

* 🐳 **Dockerized Deployment**

  * Fully containerized with PostgreSQL
  * Ready for AWS EC2 deployment

---

## 🧠 System Architecture

```text
Client → FastAPI Backend → ML Model → Decision Engine → PostgreSQL
```

---

## ⚙️ Tech Stack

* **Backend:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **ML Model:** XGBoost + Scikit-learn (Calibrated)
* **Auth:** JWT (python-jose, bcrypt)
* **Containerization:** Docker + Docker Compose
* **Deployment:** AWS EC2

---

## 🧪 Fraud Detection Logic

Each transaction is evaluated using:

### 1. ML Probability

* Predicts likelihood of fraud

### 2. Rule-Based Risk Factors

* High transaction amount
* Rapid transaction frequency (velocity)
* Short time gap between transactions

### 3. Final Risk Score

```text
Low Risk → APPROVED  
Medium Risk → REVIEW  
High Risk → REJECTED  
```

---

## 📂 Project Structure

```
fraudiq/
│
├── app/
│   ├── main.py
│   ├── db.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── router/
│   │   └── transaction.py
│
├── model_v2.pkl
├── features.pkl
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
```

---

## 🐳 Running with Docker

### 1. Clone Repository

```bash
git clone (https://github.com/SVChaithanya/risk-fuard-api)
cd riskguard-api
```

### 2. Run Containers

```bash
docker-compose up --build
```

### 3. Access API

```text
http://localhost:8000/docs
```

---

## 🔑 API Endpoints

### Auth

* `POST /auth/register`
* `POST /auth/login`

### Transactions

* `POST /transactions/` → Create transaction + fraud prediction
* `GET /transactions/history` → View transaction history

---

## 📊 Example Response

```json
{
  "transaction_id": "abc123",
  "amount": 21900,
  "time_gap_sec": 5,
  "fraud_probability": 0.017,
  "tx_count_1m": 4,
  "decision": "REVIEW"
}
```

---

## 🚀 Future Improvements

* 🔁 Redis-based rate limiting
* 📈 Real-time monitoring dashboard
* ☁️ Load balancing (Nginx / K3s)
* 🔗 Integration with credit risk (LoanIQ)

---

## ⚠️ Note

This project is built for **learning + demonstration purposes**, but follows real-world backend architecture patterns used in fintech systems.

---


