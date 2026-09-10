from fastapi_mail import FastMail, MessageSchema
from src.config.mail import conf


async def send_otp_email(
    email: str,
    otp: str,
):
    message = MessageSchema(
        subject="Your verification code",
        recipients=[email],
        body=f"""
            Hello,

            Your OTP for email verification is: {otp}

            This code is valid for 5 minutes. Do not share it with anyone.

            If you did not request this, you can safely ignore this email.

            Best regards,
            Business Advisory Platform Team
        """,
        subtype="plain",
    )

    fm = FastMail(conf)
    await fm.send_message(message)





async def send_invite_email(
    email: str,
    invite_url: str
):
    message = MessageSchema(
        subject="hello",
        recipients=[email],
        body=f"""
            Hello,

            You have been invited to join our Business Advisory Platform as a member of the Channelizing agencies.

            To complete your registration and gain access to the platform, please use the secure invitation link below:

            {invite_url}

            What happens next?
            • Create your account
            • Complete your profile information
            • Access loan application management services

            Important:
            • This invitation link is valid for 24 hours.
            • For security reasons, do not share this link with anyone else.

            If you were not expecting this invitation, you may safely ignore this email.

            We look forward to welcoming you to the platform.

            Best regards,
            Business Advisory Platform Team
        """,
        subtype="plain",
    )

    fm = FastMail(conf)
    await fm.send_message(message)