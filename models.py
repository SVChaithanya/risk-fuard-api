from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Float, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    transactions = relationship("Transaction", back_populates="user", cascade="all, delete")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))

    amount = Column(Float, nullable=False)
    time = Column(Integer, nullable=False)  # 🔥 Auto-generated time gap in seconds

    V1 = Column(Float, nullable=False)
    V2 = Column(Float, nullable=False)
    V3 = Column(Float, nullable=False)
    V4 = Column(Float, nullable=False)
    V5 = Column(Float, nullable=False)
    V6 = Column(Float, nullable=False)
    V7 = Column(Float, nullable=False)
    V8 = Column(Float, nullable=False)
    V9 = Column(Float, nullable=False)
    V10 = Column(Float, nullable=False)
    V11 = Column(Float, nullable=False)
    V12 = Column(Float, nullable=False)
    V13 = Column(Float, nullable=False)
    V14 = Column(Float, nullable=False)
    V15 = Column(Float, nullable=False)
    V16 = Column(Float, nullable=False)
    V17 = Column(Float, nullable=False)
    V18 = Column(Float, nullable=False)
    V19 = Column(Float, nullable=False)
    V20 = Column(Float, nullable=False)
    V21 = Column(Float, nullable=False)
    V22 = Column(Float, nullable=False)
    V23 = Column(Float, nullable=False)
    V24 = Column(Float, nullable=False)
    V25 = Column(Float, nullable=False)
    V26 = Column(Float, nullable=False)
    V27 = Column(Float, nullable=False)
    V28 = Column(Float, nullable=False)

    transaction_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")
    prediction = relationship("Prediction", back_populates="transaction", uselist=False, cascade="all, delete")


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    transaction_id = Column(
        UUID(as_uuid=True),
        ForeignKey("transactions.id", ondelete="CASCADE"),
        unique=True
    )

    fraud_probability = Column(Float, nullable=False)
    is_fraud = Column(Boolean, nullable=False)
    decision = Column(String, nullable=False)
    model_version = Column(String, nullable=False)
    predicted_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    transaction = relationship("Transaction", back_populates="prediction")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))

    token_hash = Column(String, nullable=False)
    expire = Column(DateTime(timezone=True), nullable=False)

    user = relationship("User", back_populates="refresh_tokens")


    