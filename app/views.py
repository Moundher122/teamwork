from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from social_django.utils import psa
from . import serlaizer
from . import models
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
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
      return Response({})
   




