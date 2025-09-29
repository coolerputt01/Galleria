from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

MAILJET_API_URL = "https://api.mailjet.com/v3/send"

@shared_task
def send_mail(email,token,username):
  subject = "Your Verification Token"
  message = f"<h2> Hi {username}</h2> <p>Verify your Galleria Secured account with the token: <b>{token}</b></p>"
  from_email = settings.DEFAULT_FROM_EMAIL
  recipient_list = [email]
  
  send_mail(subject,message,from_email,recipient_list)