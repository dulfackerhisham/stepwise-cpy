# from celery import shared_task
# from time import sleep

# from django.core.mail import send_mail
# from django.conf import settings
# from accounts.models import Account
# from .models import Order


# @shared_task
# def send_email_task(user_id, order_id):
#     """
#     fetching the user and order baseed on the provided IDs
#     !!!sending Order Confirmation Mail!!!
#     """

#     print("send email task called")

#     user = Account.objects.get(id=user_id)
#     order = Order.objects.get(id=order_id)

#     #sending email
#     subject = "StepWise Order Confirmation!!!"
#     message = f'''Hello {user.username},

#     Your order ID {order.id} has been successfully placed.

#     Here are some order details:
#     - Tracking Number: {order.tracking_no}
#     - Payment Mode: {order.payment_mode}

#     Thank you for shopping with us!

#     Best regards,
#     The StepWise Team'''
#     to_list = [user.email]
#     send_mail(subject, message, settings.EMAIL_HOST_USER, to_list, fail_silently=False)
#     print("executed")


