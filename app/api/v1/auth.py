from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.exceptions import UserAlreadyExistsError, InvalidCredentialsError
from app.schemas.user import UserOut, UserRegister, Token, UserLogin
from app.services.auth_service import AuthService
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register",
             response_model=UserOut,
             status_code=201)
async def register(
        data: UserRegister,
        db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    try:
        user = await service.register(data.email, data.password, data.role)
    except UserAlreadyExistsError:
        raise HTTPException(409, "Данный пользователь уже зарегистрирован.")
    return user

@router.post("/login",
             response_model=Token,
             status_code=200,)
async def login(
        data: UserLogin,
        db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    try:
        token = await service.login(data.email, data.password)
    except InvalidCredentialsError:
        raise HTTPException(401, "Неверные данные.")
    return Token(access_token=token)


