import hashlib
from sanic import Blueprint, response
from db import AsyncSessionLocal
from models import Payment, Account
from config import SECRET_KEY
from sqlalchemy.future import select

payments_bp = Blueprint("payments", url_prefix="/payments")

@payments_bp.post("/webhook")
async def webhook(request):
    data = request.json
    transaction_id = data.get("transaction_id")
    user_id = data.get("user_id")
    account_id = data.get("account_id")
    amount = data.get("amount")
    signature = data.get("signature")

    # Проверка подписи
    sign_str = f"{account_id}{amount}{transaction_id}{user_id}{SECRET_KEY}"
    expected_signature = hashlib.sha256(sign_str.encode()).hexdigest()
    if signature != expected_signature:
        return response.json({"error": "Invalid signature"}, status=400)

    async with AsyncSessionLocal() as session:
        # Проверяем существование платежа
        result = await session.execute(select(Payment).filter_by(transaction_id=transaction_id))
        existing_payment = result.scalar_one_or_none()
        if existing_payment:
            return response.json({"message": "Payment already processed"})

        # Проверяем счёт
        result = await session.execute(select(Account).filter_by(id=account_id, user_id=user_id))
        account = result.scalar_one_or_none()
        if not account:
            account = Account(id=account_id, user_id=user_id, balance=0)
            session.add(account)
            await session.commit()

        # Создаём платёж и начисляем сумму
        payment = Payment(transaction_id=transaction_id, user_id=user_id, account_id=account.id, amount=amount)
        account.balance += amount
        session.add(payment)
        await session.commit()

    return response.json({"message": "Payment processed"})