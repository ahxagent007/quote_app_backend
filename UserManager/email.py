import os
import smtplib

def send_mail(message, receiver_email_id):
    sender_email_id = os.getenv('sender_email_id')
    sender_email_id_password = os.getenv('sender_email_id_password')

    print(sender_email_id, sender_email_id_password)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(sender_email_id, sender_email_id_password)

    # sending the mail
    s.sendmail(sender_email_id, receiver_email_id, message)

    # terminating the session
    s.quit()