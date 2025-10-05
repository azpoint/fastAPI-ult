from uuid import UUID
from fastapi import HTTPException, status
from sqlmodel import Session, select
import bcrypt
from app.database.session import SessionDep
from app.schemas.partner_schema import DeliveryPartnerCreate, DeliveryPartnerUpdate
from app.database.models import DeliveryPartner
from app.utils import decode_access_token, generate_access_token


def password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


class DeliveryPartnerService:
    def __init__(self, session_db: Session) -> None:
        self.session_db = session_db

    def get(self, id: UUID) -> DeliveryPartner | None:
        return self.session_db.get(DeliveryPartner, id)

    def add(self, req_body: DeliveryPartnerCreate) -> DeliveryPartner:

        partner = DeliveryPartner(
            **req_body.model_dump(exclude={"password"}),
            ### Hash password
            password=password_hash(req_body.password),
        )

        self.session_db.add(partner)
        self.session_db.commit()
        self.session_db.refresh(partner)

        return partner

    def update(self, req_body: DeliveryPartnerUpdate, token: str) -> DeliveryPartner:

        payload = decode_access_token(token)
        partner_id = payload.get("id") or payload.get("user", {}).get("id")  # type: ignore

        partner = self.get(UUID(partner_id))

        if not partner:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Partner not found"
            )

        # Optional update fields
        update_data = req_body.model_dump(exclude_unset=True, exclude={"password"})

        for key, value in update_data.items():
            setattr(partner, key, value)

        # Commit updates
        self.session_db.commit()
        self.session_db.refresh(partner)

        return partner

    # Validate the credentials and return auth token
    def token(self, email: str, password: str) -> str:

        result = self.session_db.exec(
            select(DeliveryPartner).where(DeliveryPartner.email == email)
        )

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

        token = generate_access_token(
            data={"user": {"name": seller.name, "id": str(seller.id)}}
        )

        return token
