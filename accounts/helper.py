from . models import Account
from django.core.mail import send_mail
from django.conf import settings



def send_forgot_passwrod_mail(email, reset_link):
    # #sending email
    # subject = "Welcome to StepWise !!!"
    # message = f"Hello {email},\n\nTo reset your password, click the link below:\n\n{reset_link}\n This link will expire in 1 min"
    # to_list = [email]
    # send_mail(subject, message, settings.EMAIL_HOST_USER, to_list, fail_silently=False)
    # Sending email
    subject = "Welcome to StepWise !!!"
    message = f"Hello {email},\n\nTo reset your password, click the link below:\n\n{reset_link}\n This link will expire in 1 min"
    to_list = [email]

    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, to_list, fail_silently=False)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")