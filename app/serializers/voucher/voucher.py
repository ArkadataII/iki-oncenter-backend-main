from datetime import datetime, date
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field
import uuid
from app.serializers.base import BaseResponseSerialization


class VoucherFilters(BaseModel):
    code: Optional[str]
    name: Optional[str]
    coupon_code: Optional[str]
    apply_for: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]


class VoucherRequestSerialization(BaseModel):
    code: Optional[str]
    name: Optional[str]
    coupon_code: Optional[str]
    voucher_type: Optional[str]
    apply_for: Optional[str]
    scope: Optional[Dict]
    detail: Optional[Dict]
    package: Optional[list]
    units: Optional[int]
    discount_percent: Optional[float]
    discount_value: Optional[int]
    remainder: Optional[int]
    start_date: Optional[datetime]
    end_date: Optional[datetime]

    class Config:
        orm_mode = True


class VoucherResponseSerialization(BaseResponseSerialization):
    code: Optional[str]
    name: Optional[str]
    coupon_code: Optional[str]
    voucher_type: Optional[str]
    apply_for: Optional[str]
    scope: Optional[Any]
    detail: Optional[Any]
    package: Optional[list]
    units: Optional[int]
    discount_percent: Optional[float]
    discount_value: Optional[int]
    remainder: Optional[int]
    start_date: Optional[datetime]
    end_date: Optional[datetime]

    class Config:
        orm_mode = True
