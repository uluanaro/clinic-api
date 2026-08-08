from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password, create_access_token
from app.exceptions import UserAlreadyExistsError, InvalidCredentialsError
from app.models import User
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)

    async def register(self, email: str,  password: str, role: str) -> User:
        user = await self.user_repo.get_by_email(email)
        if user is not None:
            raise UserAlreadyExistsError()
        password_hash = hash_password(password)
        result = await self.user_repo.create(email, password_hash, role)
        await self.session.commit()
        return result

    async def login(self, email: str, password: str) -> str:
        user = await self.user_repo.get_by_email(email)
        if user is None:
            raise InvalidCredentialsError()
        verified_password = verify_password(password, user.password_hash)
        if not verified_password:
            raise InvalidCredentialsError()
        token = create_access_token({"sub": str(user.id), "role": user.role}, timedelta(minutes=30))
        return token
