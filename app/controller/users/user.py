import os
import logging
from datetime import datetime

from openpyxl import Workbook
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from fastapi_sqlalchemy import db

from app.helpers.security import reusable_oauth2
from app.helpers.login_manager import login_required, PermissionRequired
from app.helpers.paging import Page, PaginationParams, paginate
from app.models.users.user import User
from app.serializers.base import DataResponse
from app.serializers.users.user import UserItemResponse, UserCreateRequest, UserUpdateMeRequest, UserUpdateRequest
from app.services.base import CRUDBase
from app.services.users.user import UserService

logger = logging.getLogger()

router = APIRouter()


@router.get("")
def get(params: PaginationParams = Depends()):
    """
    API Get list User
    """
    try:
        _query = db.session.query(User).order_by(User.created_at.desc())
        users = paginate(model=User, query=_query, params=params)
        return users

    except Exception as exc:
        print(logger.error(exc))
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='BAD REQUEST')


@router.get('/export', dependencies=[Depends(reusable_oauth2)])
def getExportData(params: PaginationParams = Depends()):
    """
    API Export list User
    """
    try:
        now = f"""users{str(datetime.now().strftime('%d_%m_%Y_%H%M%S%f'))}"""
        file_name = f'{now}.xlsx'
        root_path = f'{os.getcwd()}/app/media/history'
        headers = {
            'Content-Disposition': f'attachment; filename={file_name}',
            'content_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }
        wb = Workbook()
        ws = wb.active
        ws.append(['full name'.upper(), 'email'.upper(), 'provider'.upper(), 'role'.upper(), 'is active'.upper(),
                   'last login'.upper()])

        _query = db.session.query(User)
        users = jsonable_encoder(CRUDBase(User).list(db=db, query=_query, params=params))

        data = users.get("data")

        for i in data:
            row = [i.get('full_name'), i.get('email'), i.get('provider'), i.get('role'), i.get('is_active'),
                   i.get('last_login')]
            ws.append(row)
        wb.save(f'{root_path}/{file_name}')

        return FileResponse(f'{root_path}/{file_name}', headers=headers)

    except Exception as exc:
        print(logger.error(exc))
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='BAD REQUEST')


@router.post("", response_model=DataResponse[UserItemResponse], dependencies=[Depends(reusable_oauth2)])
def create(user_data: UserCreateRequest):
    """
    API Create User
    """
    try:
        exist_user = db.session.query(User).filter(User.email == user_data.email).first()
        if exist_user:
            raise Exception('Email already exists')

        new_user = UserService().create_user(user_data)

        return DataResponse().success_response(data=new_user)

    except Exception as exc:
        print(logger.error(exc))
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='BAD REQUEST')


@router.get("/me", response_model=DataResponse[UserItemResponse], dependencies=[Depends(reusable_oauth2)])
def detail_me(Authorize: AuthJWT = Depends()):
    """
    API get detail current User
    """
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        user = db.session.query(User).get(current_user)

        return DataResponse().success_response(code=status.HTTP_200_OK, message="Thành công", data=user)

    except Exception as exc:
        print(logger.error(exc))
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='BAD REQUEST')


@router.put("/me", response_model=DataResponse[UserItemResponse], dependencies=[Depends(reusable_oauth2)])
def update_me(user_data: UserUpdateMeRequest,
              current_user: User = Depends(UserService().get_current_user)):
    """
    API Update current User
    """
    try:
        if user_data.email is not None:
            exist_user = db.session.query(User).filter(
                User.email == user_data.email, User.id != current_user.id).first()
            if exist_user:
                raise Exception('Email already exists')

        updated_user = UserService().update_me(data=user_data, current_user=current_user)

        return DataResponse().success_response(code=status.HTTP_200_OK, message="Thành công", data=updated_user)

    except Exception as exc:
        print(logger.error(exc))
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='BAD REQUEST')


@router.get("/{user_id}", response_model=DataResponse[UserItemResponse], dependencies=[Depends(reusable_oauth2)])
def detail(user_id: int):
    """
    API get Detail User
    """
    try:
        exist_user = db.session.query(User).get(user_id)

        if exist_user is None:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not exists')

        return DataResponse().success_response(data=exist_user)

    except Exception as exc:
        print(logger.error(exc))
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='BAD REQUEST')


@router.put("/{user_id}", response_model=DataResponse[UserItemResponse], dependencies=[Depends(reusable_oauth2)])
def update(user_id: int, user_data: UserUpdateRequest):
    """
    API update User
    """
    try:
        exist_user = db.session.query(User).get(user_id)
        if exist_user is None:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not exists')

        updated_user = UserService().update(user=exist_user, data=user_data)

        return DataResponse().success_response(data=updated_user)

    except Exception as exc:
        print(logger.error(exc))
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='BAD REQUEST')
