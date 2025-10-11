from fastapi import BackgroundTasks
from fastapi_mail import MessageSchema, MessageType
from pydantic import EmailStr
from app.configs.mail_config import fastmailConfig


class NotificationService:
    def __init__(self, background_tasks: BackgroundTasks) -> None:
        self.fastmail = fastmailConfig
        self.background_tasks = background_tasks

    def send_email(self, recipients: list[EmailStr], subject: str, body: str):
        message = MessageSchema(
            recipients=recipients,
            subject=subject,
            body=body,
            subtype=MessageType.plain,
        )

        # Correct: pass function + argument to background task
        self.background_tasks.add_task(self.fastmail.send_message, message)
