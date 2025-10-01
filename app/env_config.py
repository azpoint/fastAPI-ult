# POSTGRES_SERVER=127.0.0.1
# POSTGRES_PORT=""
# POSTGRES_DB=""
# POSTGRES_USER=""
# POSTGRES_PASSWORD=""
# JWT_SECRET=
# JWT_ALGORITHM=

from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_URL = f"postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_SERVER")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}"

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
