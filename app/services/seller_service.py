from sqlmodel import Session
import bcrypt
from app.schemas.seller_schema import SellerCreate
from app.database.models import Seller


def password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


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
