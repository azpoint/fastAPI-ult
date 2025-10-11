import asyncio
from mailbox import Message
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from app import env_config

conf = ConnectionConfig(
    MAIL_USERNAME=env_config.MAIL_USERNAME,  # type: ignore
    MAIL_PASSWORD=env_config.MAIL_PASSWORD,  # type: ignore
    MAIL_FROM=env_config.MAIL_FROM,  # type: ignore
    MAIL_FROM_NAME=env_config.MAIL_FROM_NAME,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_STARTTLS=True,  # use STARTTLS (required for Gmail)
    MAIL_SSL_TLS=False,  # don't use implicit SSL
    USE_CREDENTIALS=True,
)

fm = FastMail(conf)


async def send_message():
    await fm.send_message(
        message=MessageSchema(
            recipients=["thebest283@gmail.com"],
            subject="Your test mail",
            body="Fuck you and all your stupid and useless course",
            subtype=MessageType.plain,
        )
    )
    print("Email sent!")


asyncio.run(send_message())

print(env_config)
