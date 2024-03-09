import os
import smtplib

def send_mail(message, receiver_email_id):
    try:
        sender_email_id = os.getenv('sender_email_id')
        sender_email_id_password = os.getenv('sender_email_id_password')

        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)

        # start TLS for security
        s.starttls()

        # Authentication
        s.login(sender_email_id, sender_email_id_password)

        SUBJECT = "Quote App OTP"
        message = 'Subject: {}\n\n{}'.format(SUBJECT, message)

        # sending the mail
        s.sendmail(sender_email_id, receiver_email_id, message)

        # terminating the session
        s.quit()
    except Exception as e:
        print('Send Email Error: ',str(e))
