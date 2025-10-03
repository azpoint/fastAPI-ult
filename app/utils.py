from datetime import datetime, timedelta, timezone
from uuid import uuid4
from fastapi import HTTPException
from app.env_config import JWT_SECRET, JWT_ALGORITHM
import jwt


def generate_access_token(data: dict, expire: timedelta = timedelta(days=1)) -> str:
    token = jwt.encode(
        payload={
            **data,
            "jti": str(uuid4()),
            "exp": datetime.now(timezone.utc) + expire,
        },
        algorithm=JWT_ALGORITHM,
        key=JWT_SECRET,
    )

    return token


def decode_access_token(token: str) -> dict | None:
    try:
        decoded_jwt = jwt.decode(
            jwt=token,
            key=JWT_SECRET,
            algorithms=[JWT_ALGORITHM],  # type: ignore
        )

        return decoded_jwt

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired token")

    except jwt.PyJWTError:
        return None
