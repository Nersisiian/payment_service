from sanic import Blueprint, response
from db import AsyncSessionLocal
from models import User
from sqlalchemy.future import select

users_bp = Blueprint("users", url_prefix="/users")

@users_bp.get("/")
async def list_users(request):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        data = [{"id": u.id, "email": u.email, "full_name": u.full_name, "role": u.role} for u in users]
        return response.json(data)

@users_bp.post("/create")
async def create_user(request):
    data = request.json
    new_user = User(
        email=data["email"],
        password=data["password"],
        full_name=data.get("full_name", ""),
        role=data.get("role", "user")
    )
    async with AsyncSessionLocal() as session:
        session.add(new_user)
        await session.commit()
        return response.json({"message": "User created", "id": new_user.id})

@users_bp.delete("/<user_id:int>")
async def delete_user(request, user_id):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).filter_by(id=user_id))
        user = result.scalar_one_or_none()
        if not user:
            return response.json({"error": "User not found"}, status=404)
        await session.delete(user)
        await session.commit()
        return response.json({"message": "User deleted"})