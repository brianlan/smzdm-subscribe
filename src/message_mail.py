import smtplib
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .settings import auth, logger


def sendmail(subject, sender, receivers, html_texts):
    msg = MIMEMultipart()
    msg["To"] = ', '.join(receivers)
    msg["From"] = sender
    msg["Subject"] = subject

    # Attaching Text
    msg_text = MIMEText(html_texts, 'html')
    msg.attach(msg_text)   # Added, and edited the previous line

    try:
        server = smtplib.SMTP()
        server.connect(auth['mailserver']['host'])
        server.login(auth['mailserver']['username'], auth['mailserver']['password'])
        server.sendmail(sender, receivers, msg.as_string())
        server.close()
    except SMTPException as e:
        logger.error('Error when sending mail. err_msg: {}'.format(e))
