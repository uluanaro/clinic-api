from pydantic import EmailStr, BaseModel, ConfigDict


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'