import os
import jwt

from typing import Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_settings import SessionLocal
from db.modelsDB import User

basedir = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
load_dotenv(os.path.join(basedir, '.env'))

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
#SECRET_KEY = 'django-insecure-tvgl2*us)=xd^@yp9a=g*$%#cojbp%y76!2w5=7g)s4=ct%+z4'
#ALGORITHM = 'HS256'

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

async def get_current_user(
        token: Annotated[str, Depends(oauth2_schema)],
        db_session: Annotated[AsyncSession, Depends(get_db)]):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get('user_id')
        if user_id is None:
            raise credential_exception
    except JWTError:
        raise credential_exception

    user = await db_session.get(User, user_id)
    if user is None:
        raise credential_exception
    return user