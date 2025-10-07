from fastapi.security import OAuth2PasswordBearer

oauth2_scheme_seller = OAuth2PasswordBearer(
    tokenUrl="/seller/login", scheme_name="Seller_Auth"
)
