from sqlalchemy import Column, BigInteger, Integer, String, DateTime, Float, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import BaseModel


class Voucher(BaseModel):
    __tablename__ = 'voucher'

    code = Column(String, index=True, nullable=True, default=None)
    name = Column(String, index=True, nullable=True, default=None)
    coupon_code = Column(String, index=True, nullable=True, default=None)
    detail = Column(JSONB, nullable=True, default=None)
    scope = Column(JSONB, nullable=True, default=None)
    voucher_type = Column(String, nullable=True, default=None)
    apply_for = Column(String, nullable=True, default=None)
    package = Column(ARRAY(String), nullable=True, default=None)
    units = Column(BigInteger, nullable=True, default=0)
    discount_percent = Column(Float, nullable=True, default=0.0)
    discount_value = Column(BigInteger, nullable=True, default=0)
    remainder = Column(BigInteger, nullable=True, default=0)
    start_date = Column(DateTime, index=True, nullable=True, default=None)
    end_date = Column(DateTime, index=True, nullable=True, default=None)

    def __repr__(self):
        """ Show Voucher object info. """
        return '{}'.format(self.id)


class UserVoucher(BaseModel):
    __tablename__ = 'user_voucher'

    user_id = Column(BigInteger, index=True, nullable=True, default=None)
    voucher_id = Column(BigInteger, index=True, nullable=True, default=None)
    voucher_code = Column(String, index=True, nullable=True, default=None)
    coupon_code = Column(String, index=True, nullable=True, default=None)
    payment_code = Column(String, nullable=True, default=None)
    package_id = Column(BigInteger, nullable=True, default=None)
    status = Column(String, nullable=True, default=None)

    def __repr__(self):
        """ Show Voucher object info. """
        return '{}'.format(self.id)
