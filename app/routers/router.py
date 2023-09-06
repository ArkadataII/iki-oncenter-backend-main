from fastapi import APIRouter

from app.controller.auth import authorization
from app.controller.users import user
from app.controller.voucher import vouchers

router = APIRouter()

'''AUTHENTICATION SERVICE'''

router.include_router(authorization.router, tags=["Account"], prefix="/users")
router.include_router(user.router, tags=["User"], prefix="/users")
router.include_router(vouchers.router, tags=["voucher"], prefix="/voucher")
