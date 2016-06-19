import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from settings import MAIL_SERVER


def sendmail(subject, sender, receivers, html_texts):
    msg = MIMEMultipart()
    msg["To"] = ', '.join(receivers)
    msg["From"] = sender
    msg["Subject"] = subject

    # Attaching Text
    msg_text = MIMEText(html_texts, 'html')
    msg.attach(msg_text)   # Added, and edited the previous line

    smtp = smtplib.SMTP()
    smtp.connect(MAIL_SERVER)
    smtp.sendmail(sender, receivers, msg.as_string())
    smtp.quit()
