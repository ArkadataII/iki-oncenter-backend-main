from base64 import b64encode

from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import bcrypt, bcrypt_check

from sqlalchemy import Column, String, Boolean, DateTime, BigInteger, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = 'user'

    full_name = Column(String, index=True, nullable=True, default=None)
    email = Column(String, index=True, nullable=True, default=None)
    hashed_password = Column(String(255), nullable=True, default=None)
    provider = Column(String, index=True, nullable=True, default=None)
    role = Column(String, index=True, nullable=True, default='GUEST')
    auth_mode = Column(String, nullable=True, default="OAUTH")
    bio = Column(JSONB, nullable=True, default=None)
    uid = Column(String, unique=True, index=True, default=None)
    validate = Column(Boolean, default=False)
    last_login = Column(DateTime, index=True, nullable=True, default=None)
    id_facebook = Column(BigInteger, nullable=True, default=None)
    affiliate_id = Column(Integer, nullable=True)
    utm_camp = Column(String, nullable=True)

    history = relationship("History", back_populates="user")
    plagiarism = relationship("Plagiarism", back_populates="user")
    survey = relationship("Survey", back_populates="user")
    affiliate = relationship("Affiliate", back_populates="user")

    @property
    def password(self):
        return None

    @password.setter
    def password(self, val):
        self.hashed_password = self.__hash_password(val)

    def __hash_password(self, password: str):
        b64pwd = b64encode(SHA256.new(password.encode()).digest())
        return bcrypt(b64pwd, 12).decode()

    def verify_password(self, password: str):
        """
        Check if hashed password matches actual password
        """
        try:
            b64pwd = b64encode(SHA256.new(password.encode()).digest())
            bcrypt_check(b64pwd, self.hashed_password.encode())
            return True
        except ValueError:
            b64pwd = b64encode(SHA256.new(password.encode()).digest())
            print(bcrypt(b64pwd, 12).decode())
            return False
