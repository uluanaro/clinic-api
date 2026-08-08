from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.doctor import Doctor
from fastapi import HTTPException, status

from app.repositories.user_repository import UserRepository


async def get_existing_doctor(
    doctor_id: int,
    db: AsyncSession = Depends(get_db),
) -> Doctor:
    result = await db.execute(select(Doctor).where(Doctor.id == doctor_id))
    doctor = result.scalar_one_or_none()

    if doctor is None:
        raise HTTPException(status_code=404, detail="Не существует")
    return doctor

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учётные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)

    if payload is None:
        raise credentials_exception
    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    user_repo = UserRepository(db)
    result = await user_repo.get_by_id(int(user_id))
    if result is None:
        raise credentials_exception
    return result


