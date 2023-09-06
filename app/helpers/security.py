from calendar import timegm
from datetime import datetime, timezone, timedelta
from typing import Any, Union, List, Optional, Dict
import jwt
import http
import json
from fastapi import Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from pydantic import ValidationError
from passlib.context import CryptContext

from app.db.base import get_db

from app.helpers.config import settings
from app.models.users.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
reusable_oauth2 = HTTPBearer(scheme_name='Authorization')


def validate_secret_token(request: Request, auth=Depends(reusable_oauth2)) -> Union[str, Any]:
    try:
        if auth is not None:
            if str(auth.credentials).strip() == settings.X_API_KEY.strip():
                return True
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authenticate Fail")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization is not valid")

    except (jwt.PyJWTError, ValidationError) as exc:
        print(exc)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authenticate Fail")


class AuthJWTException(Exception):
    status: bool
    statusCode: int
    error: List[str]

    def __init__(self, statusCode: int = 401, status: bool = False,
                 error: Optional[List[str]] = []) -> None:
        self.statusCode = statusCode
        self.status = status
        self.error = error

    # def __repr__(self) -> str:
    #     class_name = self.__class__.__name__
    #     return f"{class_name}(statusCode={self.statusCode!r}, status={self.status!r}, error={self.error!r})"


class Authorizer:
    def __init__(self, uid: int, email: str = None, role: str = None, client_host: str = None):
        self.uid = uid
        # self.email = email
        # self.role = role
        self.client_host = client_host

    def to_dict(self):
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data.get('uid'), data.get('client_host'))


def create_access_token(uid: Union[int, Any]) -> str:
    expire = datetime.utcnow() + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS)
    to_encode = {"exp": expire, "uid": str(uid)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.SECURITY_ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def generate_token(auth: Authorizer) -> str:
    to_encode = auth.to_dict()
    to_encode.update({"exp": datetime.now(tz=timezone.utc) + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS)})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.SECURITY_ALGORITHM)
    return encoded_jwt


def generate_refresh_token(auth: Authorizer) -> str:
    to_encode = auth.to_dict()
    to_encode.update({"exp": datetime.now(tz=timezone.utc) + timedelta(seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS)})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_SECRET_KEY, algorithm=settings.SECURITY_ALGORITHM)
    return encoded_jwt


def is_exp(token):
    now = timegm(datetime.now(tz=timezone.utc).utctimetuple())
    return now > token['exp']


def validate_token(request: Request, auth=Depends(reusable_oauth2)) -> Union[str, Any]:
    """
    Decode JWT token to get user info
    """
    try:
        if auth is not None:
            lee_time = 60
            payload = jwt.decode(auth.credentials, settings.SECRET_KEY, leeway=timedelta(seconds=lee_time),
                                 algorithms=[settings.SECURITY_ALGORITHM])
            if is_exp(payload):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Refresh token before 60s remaining")

            request.state.user = Authorizer.from_dict(payload)
            return request.state.user
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization is not valid")

    except (jwt.PyJWTError, ValidationError) as exc:
        print(exc)
        # raise AuthJWTException(statusCode=status.HTTP_401_UNAUTHORIZED, status=False,
        #                        error=["Could not validate credentials", ])
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


def validate_refresh_token(request: Request, auth=Depends(reusable_oauth2)) -> Union[str, Any]:
    """
    Decode JWT token to get user info
    """
    try:
        if auth is not None:
            payload = jwt.decode(auth.credentials, settings.JWT_REFRESH_SECRET_KEY,
                                 algorithms=[settings.SECURITY_ALGORITHM])
            if is_exp(payload):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")

            request.state.user = Authorizer.from_dict(payload)
            return request.state.user
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization is not valid")

    except (jwt.PyJWTError, ValidationError) as exc:
        print(exc)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


class AuthChecker:
    def __is_valid(self, role):
        return role.lower() in self.roles

    def __init__(self, roles):
        self.roles = roles

    def __call__(self, request: Request, user: Authorizer = Depends(validate_token), db: Session = Depends(get_db)):
        auth_info = jsonable_encoder(request.state.user)
        uid = auth_info.get('uid')
        current_user = db.query(User.role).filter_by(uid=uid).first()

        if current_user is not None and current_user.role is not None and self.__is_valid(current_user.role):
            return user
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="You have no right to access this resource")


# validate_admin = AuthChecker([User.ROLE_ADMIN.lower()])
# validate_manager = AuthChecker([User.ROLE_ADMIN.lower(), User.ROLE_MANAGER.lower()])
# validate_agency = AuthChecker([User.ROLE_ADMIN.lower(), User.ROLE_MANAGER.lower(), User.ROLE_AGENCY.lower()])
# validate_user = AuthChecker([User.ROLE_ADMIN.lower(), User.ROLE_MANAGER.lower(), User.ROLE_GUEST.lower()])
