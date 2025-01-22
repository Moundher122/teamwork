from django.urls import path,include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('auth/', include('social_django.urls')),
    path('refreshtoken',TokenRefreshView.as_view()),
    path('Login',views.Login.as_view()),
    path('Signin',views.Signin.as_view())
]

