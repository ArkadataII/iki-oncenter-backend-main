from typing import Optional, Union, Any

from fastapi import Depends
from fastapi_sqlalchemy import db
from fastapi_jwt_auth import AuthJWT

from app.helpers.security import verify_password, get_password_hash
from app.models.users.user import User
from app.serializers.users.user import (UserCreateRequest, UserCreateSSRequest, UserUpdateMeRequest,
                                        UserUpdateRequest, UserRegisterRequest)


class UserService(object):
    __instance = None

    @staticmethod
    def authenticate(*, email: str, password: str) -> Optional[User]:
        """
        Check username and password is correct.
        Return object User if correct, else return None
        """
        user = db.session.query(User).filter_by(email=email).first()

        if not user:

            return None

        if not verify_password(password, user.hashed_password):

            return None

        return user

    @staticmethod
    def authenticateGoogle(*, email: str, provider: str, id_facebook: str) -> Optional[User]:
        """
        Check username and password is correct.
        Return object User if correct, else return None
        """
        user = db.session.query(User).filter_by(email=email, provider=provider, id_facebook=id_facebook).first()

        if not user:

            return None

        return user
    
    @staticmethod    
    def authenticateFacebook(*, email: str, provider: str, id_facebook: str) -> Optional[User]:
        """
        Check username and password is correct.
        Return object User if correct, else return None
        """
        if email is not None:
            user = db.session.query(User).filter_by(email=email, provider=provider).first()
        else:
            user = db.session.query(User).filter_by(provider=provider, id_facebook=id_facebook).first()
        if not user:
            return None
        return user

    @staticmethod
    async def get_current_user(user_id):
        """
        Decode JWT token to get user_id => return User info from DB query
        """

        current_user = db.session.query(User).filter_by(id=user_id).first()

        return current_user

    @staticmethod
    def register_user(data: UserRegisterRequest):
        register_user = User(
            full_name=data.full_name,
            email=data.email,
            hashed_password=get_password_hash(data.password),
            is_active=True,
            role=data.role.value
        )

        db.session.add(register_user)
        db.session.commit()

        return register_user

    @staticmethod
    def create_user(data: UserCreateRequest):
        new_user = User(
            full_name=data.full_name,
            email=data.email,
            hashed_password=get_password_hash(data.password),
            is_active=data.is_active,
            role=data.role.value,
        )

        db.session.add(new_user)
        db.session.commit()

        return new_user

    @staticmethod
    def create_user_ss(data: UserCreateSSRequest):
        new_user = User(
            full_name=data.full_name,
            email=data.email,
            provider=data.provider,
            id_facebook=data.id_facebook,
            is_active=data.is_active,
            role=data.role.value,
        )
        print("new_user", new_user)
        db.session.add(new_user)
        db.session.commit()

        return new_user

    @staticmethod
    def update_me(data: UserUpdateMeRequest, current_user: User):
        current_user.full_name = current_user.full_name if data.full_name is None else data.full_name
        current_user.email = current_user.email if data.email is None else data.email
        current_user.hashed_password = current_user.hashed_password if data.password is None else get_password_hash(
            data.password)

        db.session.commit()

        return current_user

    @staticmethod
    def update(user: User, data: UserUpdateRequest):
        user.full_name = user.full_name if data.full_name is None else data.full_name
        user.email = user.email if data.email is None else data.email
        user.hashed_password = user.hashed_password if data.password is None else get_password_hash(
            data.password)
        user.is_active = user.is_active if data.is_active is None else data.is_active
        user.role = user.role if data.role is None else data.role.value

        db.session.commit()

        return user
