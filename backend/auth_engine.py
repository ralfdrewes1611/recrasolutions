"""
Auth Engine — Wachtwoordbeveiliging voor RECRA platform.
Simpele admin login met JWT tokens.
"""
import os
import bcrypt
import jwt
import logging
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel

logger = logging.getLogger("auth")
auth_router = APIRouter(prefix="/auth", tags=["Auth"])

JWT_ALGORITHM = "HS256"


def get_jwt_secret():
    return os.environ["JWT_SECRET"]


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
        "type": "access",
    }
    return jwt.encode(payload, get_jwt_secret(), algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, get_jwt_secret(), algorithms=[JWT_ALGORITHM])
        if payload.get("type") != "access":
            return None
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


# Admin credentials from env
_admin_hash = None


def _get_admin_hash():
    global _admin_hash
    if _admin_hash is None:
        pw = os.environ.get("ADMIN_PASSWORD", "Welkom123$")
        _admin_hash = hash_password(pw)
    return _admin_hash


def _get_admin_username():
    return os.environ.get("ADMIN_USERNAME", "AdminRECRA")


class LoginRequest(BaseModel):
    username: str
    password: str


@auth_router.post("/login")
async def login(req: LoginRequest, response: Response):
    """Login met gebruikersnaam en wachtwoord."""
    admin_user = _get_admin_username()
    admin_hash = _get_admin_hash()

    if req.username != admin_user:
        raise HTTPException(status_code=401, detail="Ongeldige gebruikersnaam of wachtwoord")

    if not verify_password(req.password, admin_hash):
        raise HTTPException(status_code=401, detail="Ongeldige gebruikersnaam of wachtwoord")

    token = create_access_token(req.username)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=86400,
        path="/",
    )

    return {
        "token": token,
        "username": admin_user,
        "role": "admin",
    }


@auth_router.get("/me")
async def get_me(request: Request):
    """Check huidige sessie."""
    token = request.cookies.get("access_token")
    if not token:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
    if not token:
        raise HTTPException(status_code=401, detail="Niet ingelogd")

    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Sessie verlopen")

    return {
        "username": payload["sub"],
        "role": "admin",
    }


@auth_router.post("/logout")
async def logout(response: Response):
    """Uitloggen — cookie verwijderen."""
    response.delete_cookie("access_token", path="/")
    return {"message": "Uitgelogd"}
