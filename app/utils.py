from datetime import datetime, timedelta
from app.env_config import JWT_SECRET, JWT_ALGORITHM
import jwt


def generate_access_token(data: dict, expire: timedelta = timedelta(days=1)) -> str:
    token = jwt.encode(
        payload={**data, "exp": datetime.now() + expire},
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
    except jwt.PyJWTError:
        return None

    return decoded_jwt
