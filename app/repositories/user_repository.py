from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import User


class UserRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        user = await self.session.execute(select(User).where(User.email == email))
        return user.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> User | None:
        user = await self.session.execute(select(User).where(User.id == user_id))
        return user.scalar_one_or_none()

    async def create(self, email: str, password_hash: str, role: str) -> User:
        user = User(email=email, password_hash=password_hash, role=role)
        self.session.add(user)
        await self.session.flush()
        return user
