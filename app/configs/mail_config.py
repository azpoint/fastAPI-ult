from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from app.configs import env_config

conf = ConnectionConfig(
    MAIL_USERNAME=env_config.MAIL_USERNAME,  # type: ignore
    MAIL_PASSWORD=env_config.MAIL_PASSWORD,  # type: ignore
    MAIL_FROM=env_config.MAIL_FROM,  # type: ignore
    MAIL_FROM_NAME=env_config.MAIL_FROM_NAME,
    MAIL_SERVER=env_config.MAIL_SERVER,  # type: ignore
    MAIL_PORT=587,
    MAIL_STARTTLS=True,  # use STARTTLS (required for Gmail)
    MAIL_SSL_TLS=False,  # don't use implicit SSL
    USE_CREDENTIALS=True,
)

fastmailConfig = FastMail(conf)
