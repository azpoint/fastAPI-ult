from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlmodel import Session, select
from app.config import JWT_SECRET
import bcrypt
import jwt
from app.schemas.seller_schema import SellerCreate
from app.database.models import Seller


def password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


class SellerService:
    def __init__(self, session_db: Session) -> None:
        self.session_db = session_db

    async def add(self, credentials: SellerCreate) -> Seller:

        seller = Seller(
            **credentials.model_dump(exclude={"password"}),
            ### Hash password
            password=password_hash(credentials.password)
        )

        self.session_db.add(seller)
        self.session_db.commit()
        self.session_db.refresh(seller)

        return seller

    # Validate the credentials and return auth token
    async def login(self, email: str, password: str) -> str:

        result = self.session_db.exec(select(Seller).where(Seller.email == email))

        seller = result.first()

        if seller is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller not found",
            )

        # Verify password
        if not verify_password(password, seller.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password or email",
            )

        token = jwt.encode(
            payload={
                "user": {"name": seller.name, "email": seller.email},
                "exp": datetime.now() + timedelta(days=1),
            },
            algorithm="HS256",
            key=JWT_SECRET,
        )

        return token
