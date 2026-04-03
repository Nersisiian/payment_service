from sanic import Blueprint, response
from db import AsyncSessionLocal
from models import User, Account
from sqlalchemy.future import select

accounts_bp = Blueprint("accounts", url_prefix="/accounts")

@accounts_bp.get("/user/<user_id:int>")
async def list_user_accounts(request, user_id):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Account).filter_by(user_id=user_id))
        accounts = result.scalars().all()
        data = [{"id": a.id, "balance": a.balance} for a in accounts]
        return response.json(data)

@accounts_bp.get("/")
async def list_all_accounts(request):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Account))
        accounts = result.scalars().all()
        data = [{"id": a.id, "user_id": a.user_id, "balance": a.balance} for a in accounts]
        return response.json(data)