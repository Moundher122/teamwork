
from celery import shared_task
from django.core.mail import send_mail
@shared_task
def sendemail(title,subject,message,to):
     subject = subject  
     html_message = f"""
     <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); padding: 20px;">
                <h1 style="color: #4CAF50; text-align: center;">{title}</h1>
                <p style="color: #333333; font-size: 16px; line-height: 1.6;">{message}</p>
                <p style="text-align: center; margin-top: 20px; color: #4CAF50;">Best regards, <br> The Team</p>
            </div>
        </body>
    </html>
    """
    
     from_email = 'bouroumanamoundher@gmail.com'
     recipient_list = [to]
     send_mail(subject, message, from_email, recipient_list, html_message=html_message)