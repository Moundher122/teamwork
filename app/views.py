from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from social_django.utils import psa
from . import serlaizer
from . import models
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from projectcore import settings
from django.template.loader import render_to_string
from django.http import HttpResponse
class GoogleLoginView(APIView):
    @psa('social:complete')
    def get(self, request, *args, **kwargs):
        user = request.user
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        return Response({
            'access_token': str(access_token),
            'refresh_token': str(refresh),
        })
class Login(APIView):
    def post(self, request):
        user=request.data
        ser=serlaizer.UserSerializer(data=user)
        if ser.is_valid():
            ser.save()
            us=models.User.objects.get(id=ser.data['id'])
            us.set_password(user['password'])
            us.save()
            refresh=RefreshToken.for_user(us)
            access_token=refresh.access_token
            return Response({
                'user':ser.data,
                'acess_token':str(access_token),
                'refresh_token':str(refresh)
            })
        return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
class Signin(APIView):
    def post(self,request):
        username=request.data.get('username')
        email=request.data.get('email')
        password=request.data.get('password')
        try:
         if username :
            user=models.User.objects.get(username=username )
         elif email:
            user=models.User.objects.get(email=email)
         if email or username:
            ser=serlaizer.UserSerializer(user)
            if user.check_password(password):
             refresh=RefreshToken.for_user(user)
             AccessToken=refresh.access_token
             return Response({
                'user':ser.data,
                'access_token':str(AccessToken),
                'Refresh-tokrn':str(refresh)
             })
            return Response({'wrong password'})
        except models.User.DoesNotExist:
           return Response({'user DosentExist'})

class deleteaccount(APIView):
   permission_classes=[IsAuthenticated]
   def delete(self,request):
      user=request.user
      user.delete()
      return Response({'acount deleted'})

class test(APIView):
    def post(self,request):
     subject = 'Custom HTML Email with Styles'
     message = 'This is a plain text fallback message.'
     text='wee neeed u'
    # HTML content with inline CSS for custom styles
     html_message = f"""
     <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); padding: 20px;">
                <h1 style="color: #4CAF50; text-align: center;">{text}</h1>
                <p style="color: #333333; font-size: 16px; line-height: 1.6;">Thank you for signing up. We are excited to have you on board. Please find more details below:</p>
                <div style="background-color: #f0f0f0; border-left: 5px solid #4CAF50; padding: 15px; margin-top: 20px;">
                    <h3 style="color: #333333;">Important Information</h3>
                    <ul style="color: #333333; list-style-type: none; padding-left: 0;">
                        <li>Get started by exploring your dashboard.</li>
                        <li>Check out our documentation for detailed guides.</li>
                        <li>Contact support if you need any assistance.</li>
                    </ul>
                </div>
                <p style="text-align: center; margin-top: 20px; color: #4CAF50;">Best regards, <br> The Team</p>
            </div>
        </body>
    </html>
    """
    
     from_email = 'bouroumanamoundher@gmail.com'
     recipient_list = ['bouroumamoundher@gmail.com']
     send_mail(subject, message, from_email, recipient_list, html_message=html_message)


class addfile(APIView):
   permission_classes=[IsAuthenticated]
   def post(self,request):
      pass





