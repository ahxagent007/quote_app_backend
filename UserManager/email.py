import smtplib

def send_mail(message, receiver_email_id):
    sender_email_id = 'alphacuetechnologies@gmail.com'
    sender_email_id_password = 'AlphaCueTechXiAn2023'

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