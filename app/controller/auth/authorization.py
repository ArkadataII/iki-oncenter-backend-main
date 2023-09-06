from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Depends, status, Request, Response
from fastapi_sqlalchemy import db
from fastapi_jwt_auth import AuthJWT

from app.helpers.security import reusable_oauth2
from app.helpers.config import settings
from app.models.users.user import User
from app.serializers.base import DataResponse
from app.serializers.account.token import Token
from app.serializers.users.user import (UserCreateSSRequest, UserItemResponse, UserRegisterRequest, LoginRequest,
                                        SSLoginRequest)
from app.services.users.user import UserService

router = APIRouter()


@router.post('/login', response_model=DataResponse[Token])
async def login_access_token(form_data: LoginRequest, Authorize: AuthJWT = Depends()):
    try:
        user = UserService().authenticate(email=form_data.username, password=form_data.password)

        if not user.is_active:
            return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Inactive User')

        user.last_login = datetime.now()
        db.session.commit()

        expires = settings.ACCESS_TOKEN_EXPIRE_SECONDS
        one_day = 60 * 60 * 24
        access_token = Authorize.create_access_token(subject=user.id, expires_time=expires)
        refresh_token = Authorize.create_refresh_token(subject=user.id, expires_time=expires + one_day)

        return DataResponse().success_response({
            'access_token': access_token,
            "refresh_token": refresh_token
        })

    except Exception as exc:
        print(str(exc))
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='BAD REQUEST')


@router.post("/ss-login", response_model=DataResponse[Token])
def authentication(form_data: SSLoginRequest, Authorize: AuthJWT = Depends()):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        # users =id_token.verify_oauth2_token(form_data.token, requests.Request(), "138803847142-0a3d18uif6neml519g5nt6r20t9nem8e.apps.googleusercontent.com")
        dt = datetime.now()
        dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        expires = settings.ACCESS_TOKEN_EXPIRE_SECONDS
        one_day = 60 * 60 * 24
        if form_data.provider == 'facebook':
            user_ss = UserService().authenticateFacebook(email=form_data.email, provider=form_data.provider, id_facebook=form_data.id_facebook)
        else: 
            user_ss = UserService().authenticateGoogle(email=form_data.email, provider=form_data.provider)

        if user_ss is None:
            data = UserCreateSSRequest(
                full_name=form_data.fullname,
                email=form_data.email,
                provider=form_data.provider,
                id_facebook=form_data.id_facebook,
            )

            register_user = UserService().create_user_ss(data)
            register_user.last_login = datetime.now()
            db.session.commit()
            access_token = Authorize.create_access_token(subject=register_user.id, expires_time=expires)
            refresh_token = Authorize.create_refresh_token(subject=register_user.id, expires_time=expires + one_day)
            return DataResponse().success_response({
                'access_token': access_token,
                "refresh_token": refresh_token
            })
        else:
            user_ss.last_login = datetime.now()
            db.session.commit()
            access_token = Authorize.create_access_token(subject=user_ss.id, expires_time=expires)
            refresh_token = Authorize.create_refresh_token(subject=user_ss.id, expires_time=expires + one_day)

            return DataResponse().success_response({
                'access_token': access_token,
                "refresh_token": refresh_token
            })

    except ValueError:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')


@router.post('/register', response_model=DataResponse[UserItemResponse])
async def register(register_data: UserRegisterRequest):
    try:
        exist_user = db.session.query(User).filter(User.email == register_data.email).first()

        if exist_user:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email Already Exists")

        register_user = UserService().register_user(register_data)

        return DataResponse().success_response(data=register_user)

    except Exception as exc:
        print(str(exc))
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='BAD REQUEST')


@router.post('/refresh', dependencies=[Depends(reusable_oauth2)], response_model=DataResponse[Token])
async def refresh(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        user_id = Authorize.get_jwt_subject()
        current_user = db.session.query(User).filter_by(id=user_id).first()

        expires = settings.ACCESS_TOKEN_EXPIRE_SECONDS
        one_day = 60 * 60 * 24

        new_access_token = Authorize.create_access_token(subject=current_user.id, expires_time=expires)
        refresh_token = Authorize.create_refresh_token(subject=current_user.id,
                                                       expires_time=expires + one_day)

        return DataResponse().success_response({
            'access_token': new_access_token,
            "refresh_token": refresh_token
        })

    except Exception as exc:
        print(str(exc))
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='BAD REQUEST')
