# Define the GET API route
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

import models
import sqlalchemy as sa

router = APIRouter()
engine = sa.create_engine("mysql+mysqlconnector://root:andry@localhost:3306/ecom")  # Replace with your database URL


# Dépendance pour injecter une session SQLAlchemy
async def get_db_session(engine):
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


@router.get("/orders")
async def get_orders():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM ecom.order"))  # Assuming a table named 'orders'
        orders = []
        for row in result.fetchall():
            # Convert row to dictionary
            order_dict = {key: value for key, value in zip(result.keys(), row)}
            # Create OrderResponse instance
            orders.append(order_dict)
    return orders


@router.get("/orders/{order_id}")
async def get_order_by_id(order_id: str):
    print(order_id)
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM ecom.order WHERE ecom.order.OrderId = '{order_id}'"))  # Assuming a table named 'orders'
        # Convert row to dictionary
        for row in result.fetchall():
            # Convert row to dictionary
            order_dict = {key: value for key, value in zip(result.keys(), row)}
    return order_dict


@router.get("/healthcheck", response_model=models.HealthResponse)
async def healthcheck():
    """
    Endpoint de vérification de l'état de l'API.

    **Réponse:**

    * Version de l'API (str)
    """
    return {"version": "1.0.0"}
