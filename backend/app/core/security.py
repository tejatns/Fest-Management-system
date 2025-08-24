"""Black-box security shortcuts to generate JWT tokens and password hashing and verifcation."""

import jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.core import config
from app.schemas.responses import AccessTokenResponse

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECS = config.settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
REFRESH_TOKEN_EXPIRE_SECS = config.settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60
PWD_CONTEXT = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=config.settings.SECURITY_BCRYPT_ROUNDS,
)


class JWTTokenPayload(BaseModel):
    """Pydantic model for JWT token payload"""

    token: str
    


def create_jwt_token(email: str, password: str):
    """Creates jwt access or refresh token for user.

    Args:
        subject: anything unique to user, id or email etc.
        exp_secs: expire time in seconds
        refresh: if True, this is refresh token
    """

    to_encode: dict[str, str] = {"email": email, "password": password}
    encoded_jwt = jwt.encode(
        to_encode,
        key=config.settings.SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies plain and hashed password matches

    Applies passlib context based on bcrypt algorithm on plain passoword.
    It takes about 0.3s for default 12 rounds of SECURITY_BCRYPT_DEFAULT_ROUNDS.
    """
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Creates hash from password

    Applies passlib context based on bcrypt algorithm on plain passoword.
    It takes about 0.3s for default 12 rounds of SECURITY_BCRYPT_DEFAULT_ROUNDS.
    """
    return PWD_CONTEXT.hash(password)
