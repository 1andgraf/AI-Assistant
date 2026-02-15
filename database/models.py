from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    telegram_id = Column(Integer, primary_key=True)
    username = Column(String)
    full_name = Column(String)
    preferences = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)

    events = relationship("Event", back_populates="user")
    expenses = relationship("Expense", back_populates="user")
    cart = relationship("CartItem", back_populates="user")
    plans = relationship("Plan", back_populates="user")

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.telegram_id'))
    title = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="events")

class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.telegram_id'))
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="expenses")

class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.telegram_id'))
    item_name = Column(String, nullable=False)
    quantity = Column(String, default="1")
    is_bought = Column(Integer, default=0) # 0 = false, 1 = true
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="cart")

class Plan(Base):
    __tablename__ = 'plans'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.telegram_id'))
    type = Column(String, nullable=False) # 'nutrition', 'training'
    content = Column(String, nullable=False) # JSON or Markdown content
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="plans")
