import logging

from django.core import mail

logger = logging.getLogger(__name__)

def send_email(to, subject, message):
    try: 
        mail.send_mail(
            subject=subject,
            message=message,
            from_email="investment_war_room@iwr.com",
            recipient_list=[to],
            html_message=message
        )

        return True

    except Exception:
        logger.exception("Something whent wrong when trying to send an email")
        return False
