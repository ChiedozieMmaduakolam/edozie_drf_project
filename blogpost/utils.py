import smtplib
import ssl
from email.message import EmailMessage
from .models import CustomUser, OneTimePassword
import random
import string
import threading


global sender
global password

sender = 'chiedoziedavidehirim@gmail.com'
password = 'ogeapajgdeybegnu'



def generate_otp():
    character_set = string.ascii_lowercase + string.ascii_uppercase + string.digits
    code = ''.join(random.sample(character_set, 8))
    return code

def send_normal_mail(receiver, subject, body):
    em = EmailMessage()
    em['From'] = sender
    em['To'] = receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', port=465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, em.as_string())


def send_code_to_user(email):
    subject = 'Email Verification For DRF Project'
    code = generate_otp()
    user = CustomUser.objects.get(email=email)
    OneTimePassword.objects.create(user=user, otp_code=code)
    body = f'Hello {user.username}, thanks for signing up. Please verify your email address with the code below \n {code}'
    send_normal_mail(receiver=email, subject=subject, body=body)

def async_send_otp(email):
    thread = threading.Thread(target=send_code_to_user, args=(email,))
    thread.start()

    
def async_send_normal_mail(receiver, subject, body):
    thread = threading.Thread(target=send_normal_mail, args=(receiver, subject, body,))
    thread.start()