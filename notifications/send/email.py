import smtplib
import os
from email.message import EmailMessage
import json


def notification(message):
    try:
        message = json.loads(message)
        mp3_fid = message['mp3_fid']
        sender_email = os.environ['GMAIL_ADDRESS']
        sender_password = os.environ['GMAIL_PASSWORD']
        receiver_email = message['message']
        msg = EmailMessage()
        msg.set_content(f"mp3 file_id : {mp3_fid} is now ready")

        msg["Subject"] = "mp3 download"
        msg["From"] = sender_email
        msg["To"] = receiver_email

        session = smtplib.SMTP("smtp.gmail.com")
        session.starttls()
        session.login(sender_email, sender_password)
        session.send_message(msg, sender_email, receiver_email)
        session.quit()
        print("Email sent successfully")
    except Exception as e:
        print(e)
        return
