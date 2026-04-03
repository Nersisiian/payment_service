import asyncio
from db import engine, Base, AsyncSessionLocal
from models import User, Account
from sqlalchemy.future import select

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Создаём тестовых пользователя и администратора
    async with AsyncSessionLocal() as session:
        user = User(email="user@example.com", password="userpass", full_name="Test User")
        admin = User(email="admin@example.com", password="adminpass", full_name="Test Admin", role="admin")
        session.add_all([user, admin])
        await session.commit()

        # Создаём счёт для пользователя
        account = Account(user_id=user.id, balance=100)
        session.add(account)
        await session.commit()

    print("База данных и тестовые данные созданы!")

if __name__ == "__main__":
    asyncio.run(init_db())