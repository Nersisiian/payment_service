from sanic import Blueprint, response
from db import AsyncSessionLocal
from models import User
from sqlalchemy.future import select

auth_bp = Blueprint("auth", url_prefix="/auth")

@auth_bp.post("/login")
async def login(request):
    data = request.json
    email = data.get("email")
    password = data.get("password")

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).filter_by(email=email, password=password))
        user = result.scalar_one_or_none()
        if not user:
            return response.json({"error": "Invalid credentials"}, status=401)

        return response.json({
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role
        })