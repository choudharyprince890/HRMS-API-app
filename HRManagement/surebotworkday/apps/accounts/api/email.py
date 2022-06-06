
from django.core.mail import send_mail
import random
from surebotworkday.settings import base 
from surebotworkday.apps.accounts.models import ResetPasswordOtp


# def send_otp():
#         subject = 'password reset otp'
#         otp = random.randrange(1000,9999, 3)
#         print(otp)

#         # email_from = base.EMAIL_HOST
#         email_from = 'testpurposeemail890@gmail.com'
#         message = f'your otp is {otp}'
#         send_mail(subject, message, email_from, ['choudharyprince890@gmail.com'], fail_silently=False,)



def send_otp(email):
        subject = 'password reset otp'
        otp = random.randrange(1000,9999, 3)
        print(otp)

        print(email.pk)
        exist = ResetPasswordOtp.objects.filter(user_id = email.pk)
        email_from = base.EMAIL_HOST_USER
        print('exists ', exist)
        if len(exist) == 0:  
                print('went in if part ')
                resetpassword = ResetPasswordOtp.objects.create(otp=otp,user=email)
                message = f'your otp is {otp}'
                print('this is the to email',email.email)
                send_mail(subject, message, email_from, [email.email])
        else:
                ResetPasswordOtp.objects.filter(user_id = email.pk).update(otp=otp,user=email)
                message = f'your otp is {otp}'
                print('this is the to email',email.email,message)
                send_mail(subject, message, email_from, [email.email])              





