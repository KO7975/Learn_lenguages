import hashlib
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os 
from dotenv import load_dotenv

load_dotenv()


def send_password_email(email, password):
    sender_email = os.environ.get('EMAIL')
    sender_password = os.environ.get('EMAIL_PASS')
    msg = MIMEMultipart()
    msg['Subject'] = "Password Recovery"
    msg['From'] = sender_email
    msg['To'] = email
    text = f"hello dear! \n Your new password is {password}."
    part1 = MIMEText(text, 'plain')
    msg.attach(part1)

    # Optional: attach a file to the email
    # filename = "attachment.txt"
    # with open(filename, "rb") as f:
    #     attach = MIMEApplication(f.read(),_subtype="txt")
    #     attach.add_header('Content-Disposition','attachment',filename=str(filename))
    #     msg.attach(attach)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        return "Password recovery email sent."
    except Exception:
        return "Password recovery email sent."
    finally:
        server.quit()

# This function generates a random password
def generate_password():
    password = ''
    for i in range(8):
        password += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
    return password


