import logging
import uuid
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, Response

from app.db.base import get_db
from app.services.base import CRUDBase
from app.helpers.security import reusable_oauth2
from app.helpers.paging import Page, PaginationParams
from app.models.voucher.voucher import Voucher
from app.serializers.base import DataResponse
from app.serializers.voucher.voucher import VoucherFilters, VoucherRequestSerialization, VoucherResponseSerialization

logger = logging.getLogger()
router = APIRouter()


@router.get("", dependencies=[Depends(reusable_oauth2)], response_model=Page[VoucherResponseSerialization])
async def get(filters: VoucherFilters = Depends(), page: PaginationParams = Depends(), db: Session = Depends(get_db)):
    try:
        _filters = filters.dict()
        list_filters = [i for i in _filters if _filters[i] is not None]

        if not list_filters:
            statement = db.query(Voucher).filter(Voucher.is_active==True)
            response = CRUDBase(Voucher).list(db=db, query=statement, params=page)
        else:
            statement = db.query(Voucher).filter(Voucher.is_active==True)

            for attr, value in _filters.items():
                if attr in list_filters:
                    statement = statement.filter(getattr(Voucher, attr).like("%%%s%%" % value))

            response = CRUDBase(Voucher).list(db=db, query=statement, params=page)

        return response

    except Exception as exc:
        print(exc)
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='BAD REQUEST')


@router.get("/{id}", dependencies=[Depends(reusable_oauth2)], response_model=DataResponse[VoucherResponseSerialization])
async def detail(id: int, db: Session = Depends(get_db)):
    try:
        response = CRUDBase(Voucher).get(db=db, id=id)

        if response is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Objects does not exist")

        return DataResponse().success_response(response)

    except Exception as exc:
        print(exc)
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='BAD REQUEST')


@router.post("", dependencies=[Depends(reusable_oauth2)], response_model=DataResponse[VoucherResponseSerialization])
async def create(req: VoucherRequestSerialization, db: Session = Depends(get_db)):
    try:
        req.code = 'voc_' + str(uuid.uuid4().hex)
        response = CRUDBase(Voucher).create(db=db, obj_in=req)

        return DataResponse().success_response(data=response)

    except Exception as exc:
        print(exc)
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='BAD REQUEST')


@router.put("/{id}", dependencies=[Depends(reusable_oauth2)], response_model=DataResponse[VoucherResponseSerialization])
async def update(id: int, req: VoucherRequestSerialization, db: Session = Depends(get_db)):
    try:
        voucher = CRUDBase(Voucher).get(db=db, id=id)

        if voucher is None:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Objects does not exist")

        response = CRUDBase(Voucher).update(db=db, db_obj=voucher, obj_in=req)

        return DataResponse().success_response(data=response)

    except Exception as exc:
        print(exc)
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='BAD REQUEST')
